import argparse
import configparser
import logging
import os
import sys

import dotted_dict

from utils.Singleton import singleton
from utils.RunUtils import is_pytest_running


def get_project_dir(subdir: str = None):
    """
    It makes easy to address project dir.

    May be used for testcases.

    Args:
        subdir (str): append specified subfolder if any

    Returns:
        (str) Absolute path for project dir with specified subdirectory if any.
    """
    if subdir is not None and os.path.isabs(subdir):
        return subdir

    proj_dir = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.abspath(os.path.join(proj_dir, '..'))
    if subdir:
        return os.path.join(proj_dir, subdir)
    else:
        return proj_dir


class Config:
    """
    Configuration storage that reads data from (from high to low priority):
    - command line
    - environment variables
    - configuration file
    If a value for specific key not found then default value is used.

    You can use dot notation to access specific values.

    There are the following values:
    config     - name of configuration file
    dir        - directory to keep files
    autocreate - create subdirs to keep files as requested
    log.level  - logging level
    log.file   - log filename
    port       - port for web-server
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger('config')
        self._env_prefix = 'SERVER'
        self._arg_parser = None
        self._args = None
        self.data = dotted_dict.DottedDict()
        self._set_defaults()
        self._create_parser()

    def _set_defaults(self) -> None:
        """Set default values."""
        self.data.update({
            'config': 'config.ini',
            'dir': 'data',
            'autocreate': True,
            'log': {
                'level': 'warning',
                'file': None,  # 'server.log'
            },
            'host': '127.0.0.1',
            'port': 8080,
            'database': {
                'host': '127.0.0.1',
                'port': 5432,
                'name': 'fileserver',
                'user': 'myuser',
                'password': 'mypass', # dotted_dict considers `pass` as keyword
            },
        })

    def _read_config(self) -> None:
        """Read values from configuration file."""
        if not os.path.exists(self.data.config):
            self._logger.info(f"config file '{self.data.config}' not found")
            return
        with open(self.data.config) as stream:
            ini_parser = configparser.ConfigParser()
            ini_parser.read_string('[default]\n' + stream.read())
            ini_params = ini_parser['default']
            # TODO: enumerate all params and get rid of specific values
            self.data.dir = ini_params.get('dir', self.data.dir)
            self.data.autocreate = ini_params.getboolean('autocreate', self.data.autocreate)
            self.data.log.level = ini_params.get('log.level', self.data.log.level)
            self.data.log.file = ini_params.get('log.file', self.data.log.file)
            self.data.host = ini_params.get('host', self.data.host)
            self.data.port = ini_params.getint('port', self.data.port)
            self.data.database.host = ini_params.get('database.host', self.data.database.host)
            self.data.database.port = ini_params.getint('database.port', self.data.database.port)
            self.data.database.name = ini_params.get('database.name', self.data.database.name)
            self.data.database.user = ini_params.get('database.user', self.data.database.user)
            self.data.database.password = ini_params.get('database.pass', self.data.database.password)

    def _read_envvars(self) -> None:
        """Read values from environment variables."""
        prefix = self._env_prefix.upper()
        self.data.config = os.getenv(f'{prefix}_CONFIG', self.data.config)
        self.data.dir = os.getenv(f'{prefix}_DIR', self.data.dir)
        self.data.autocreate = os.getenv(f'{prefix}_AUTOCREATE', self.data.autocreate)
        self.data.log.level = os.getenv(f'{prefix}_LOG_LEVEL', self.data.log.level)
        self.data.log.file = os.getenv(f'{prefix}_LOG_FILE', self.data.log.file)
        self.data.host = os.getenv(f'{prefix}_HOST', self.data.host)
        self.data.port = int(os.getenv(f'{prefix}_PORT', self.data.port))
        self.data.database.host = os.getenv(f'{prefix}_DB_HOST', self.data.database.host)
        self.data.database.port = int(os.getenv(f'{prefix}_DB_PORT', self.data.database.port))
        self.data.database.name = os.getenv(f'{prefix}_DB_NAME', self.data.database.name)
        self.data.database.user = os.getenv(f'{prefix}_DB_USER', self.data.database.user)
        self.data.database.password = os.getenv(f'{prefix}_DB_PASS', self.data.database.password)

    def _create_parser(self) -> None:
        """Create command line parser.

        Command line options:
        -d --dir       - working directory (absolute or relative path).
           --autocreate - enable autocreation of subdirs
           --log-level - set verbosity level
        -l --log-file  - set log filename
        -p --port      - port for web-server
        """
        self._arg_parser = argparse.ArgumentParser()
        self._arg_parser.add_argument('-c', '--config', type=str,
                                      help=f'config filename (default: {self.data.config})')
        self._arg_parser.add_argument('-d', '--dir', type=str,
                                      help=f'working directory (default: {self.data.dir})')
        self._arg_parser.add_argument('--autocreate', type=bool,
                                      help=f'autocreate subdirs (default: {self.data.autocreate})')
        self._arg_parser.add_argument('--log-level', choices=['debug', 'info', 'warning', 'error'],
                                      help=f'Log level to console (default: {self.data.log.level})')
        self._arg_parser.add_argument('-l', '--log-file', type=str, help='Log file')
        self._arg_parser.add_argument('-H', '--host', type=str, help='Bind address (host)')
        self._arg_parser.add_argument('-p', '--port', type=int, help='Port for web-server')
        self._arg_parser.add_argument('--db-host', type=str,
            help=f'database host (default: {self.data.database.host})')
        self._arg_parser.add_argument( '--db-port', type=int,
            help=f'database port (default: {self.data.database.port})')
        self._arg_parser.add_argument( '--db-name', type=str,
            help=f'database name (default: {self.data.database.name})')
        self._arg_parser.add_argument( '--db-user', type=str,
            help=f'database user (default: {self.data.database.user})')
        self._arg_parser.add_argument( '--db-pass', type=str,
            help=f'database password (default: {self.data.database.password})')

    def _parse_arguments(self) -> None:
        """Helper method for argument parsing."""
        if is_pytest_running():
            # called from within a test run:
            # e.g. of sys.argv: pytest server
            self._args = argparse.Namespace(
                config=None,
                dir=None,
                autocreate=None,
                log_level=None,
                log_file=None,
                host=None,
                port=None,
                db_host=None,
                db_port=None,
                db_name=None,
                db_user=None,
                db_pass=None,
            )
        else:
            # called "normally"
            self._args = self._arg_parser.parse_args()

    def _read_arguments(self) -> None:
        if self._args.dir:
            self.data.dir = self._args.dir
        if self._args.autocreate:
            self.data.autocreate = self._args.autocreate
        if self._args.log_level:
            self.data.log.level = self._args.log_level
        if self._args.log_file:
            self.data.log.file = self._args.log_file
        if self._args.host:
            self.data.host = self._args.host
        if self._args.port:
            self.data.port = self._args.port
        if self._args.db_host:
            self.data.database.host = self._args.db_host
        if self._args.db_port:
            self.data.database.port = self._args.db_port
        if self._args.db_name:
            self.data.database.name = self._args.db_name
        if self._args.db_user:
            self.data.database.user = self._args.db_user
        if self._args.db_pass:
            self.data.database.password = self._args.db_pass

    def _validate(self) -> None:
        # TODO: implement
        pass

    def update(self) -> None:
        """Read values from different sources.

        CLI arguments may redefine config filename, thus we need to split the whole process of config file processing
        to separate steps:

        - _create_parser (done once)
        - _parse_arguments (find custom config filename if any)
        - _read_arguments (read values from CLI arguments)
        """
        self._set_defaults()
        self._read_envvars()
        self._parse_arguments()
        if self._args.config:
            self.data.config = self._args.config
        self._read_config()
        self._read_arguments()
        self._validate()

    def dump_config(self):
        # TODO: print to sys.file.stdout or specified file
        pass


@singleton
class LazyProxyConfig:
    """Import of Config module will done at very start.
    Program may request update value:
    - manually using .update() method
    - automatically when first invocation occurs. Automatic update may failed because:
        - no initial settings were done (e.g., chdir)
        - ???
    """

    def __init__(self):
        object.__setattr__(self, '_config', None)

    def __getattribute__(self, name):
        c = object.__getattribute__(self, '_config')
        if c is None:
            c = Config()
            c.update()
            object.__setattr__(self, '_config', c)
        return object.__getattribute__(c.data, name)

    def __setattr__(self, name, value):
        c = object.__getattribute__(self, '_config')
        if c is None:
            c = Config()
            c.update()
            object.__setattr__(self, '_config', c)
        return object.__setattr__(c.data, name, value)

data = LazyProxyConfig()
