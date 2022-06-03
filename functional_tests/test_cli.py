"""Functional tests for CLI

Imports:
    os
    subprocess
"""

import functools
import os
import platform
import shutil
import subprocess
import uuid

from main import DEFAULT_LOG_FILE as LOG_FILE

DATA_DIR = str(uuid.uuid4())
EXECUTION_TIMEOUT = 5
LOG_FILE_ALICE = os.path.join(str(uuid.uuid4()), str(uuid.uuid4())+".log")
OS_NAME = platform.system()

if OS_NAME == "Windows":
    PYTHON_EXE = os.path.join(".venv", "Scripts", "python")
elif OS_NAME == "Linux":
    PYTHON_EXE = os.path.join(".venv", "bin", "python")
else:
    raise NotImplementedError


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate(timeout=EXECUTION_TIMEOUT)
    return out, err, proc.returncode


def clean_up(func):
    """Clean up after test"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        finally:
            # Clean up after test.
            if os.path.exists(DATA_DIR):
                os.rmdir(DATA_DIR)
            log_dir = os.path.dirname(LOG_FILE)
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            if os.path.exists(LOG_FILE):
                os.remove(LOG_FILE)
            log_dir = os.path.dirname(LOG_FILE_ALICE)
            if os.path.exists(log_dir):
                shutil.rmtree(log_dir)
            if os.path.exists(LOG_FILE_ALICE):
                os.remove(LOG_FILE_ALICE)
        return result

    return wrapper


# Alice has heard about a new cool file server app.
# She downloaded the package from its homepage into a local directory.


def test_main_no_param():
    # Since Alice is an experienced user she immediately runs the main module from CLI.
    command = [PYTHON_EXE, "main.py"]
    out, err, exitcode = capture(command)

    # Alice notices an error message about some required arguments.
    assert exitcode == 2
    assert b"Run error!" in out
    assert b"error: the following arguments are required: -d/--data-directory" in err


def test_main_help_param():
    # To understand what arguments the main module gets, she runs the main module with "-h" argument.
    command = [PYTHON_EXE, "main.py", "-h"]
    out, _, exitcode = capture(command)

    # Alice sees that the app starts without errors and contains usage information.
    assert exitcode == 0
    assert b"usage:" in out


# Now Alice knows that she must provide a location of the data directory.


@clean_up
def test_main_data_dir_param():
    # So, Alice starts the app with a required argument "-d".
    command = [PYTHON_EXE, "main.py", "-d", DATA_DIR]
    _, _, exitcode = capture(command)

    # And sees that now app starts without errors.
    assert exitcode == 0

    # Also Alice notices that specified data directory exists now
    assert os.path.exists(DATA_DIR)


# Alice is also a very curious person. She wants to try an alternative argument for specifying data directory.


@clean_up
def test_main_data_dir_alt_param():
    # She starts the app again using "--data-directory" to specify the data directory.
    command = [PYTHON_EXE, "main.py", "--data-directory", DATA_DIR]
    _, _, exitcode = capture(command)

    # Again, Alice sees that the app starts without errors.
    assert exitcode == 0

    # And she notices that specified data directory was created once more time
    assert os.path.exists(DATA_DIR)


# Alice decided to run the app and check its log.


@clean_up
def test_main_default_log_created():
    # She knows from the help message that by default the log file is called {LOG_FILE}
    command = [PYTHON_EXE, "main.py", "-d", DATA_DIR, "--log-file", LOG_FILE]
    capture(command)

    assert os.path.exists(LOG_FILE)


# Alice does not like the default name of the log file and decided to change it to "logs/alice_server.log".


@clean_up
def test_main_log_file_alt_param():
    # She runs the app with the additional option "--log-file" to specify a new name of the log file.
    command = [PYTHON_EXE, "main.py", "-d", DATA_DIR, "--log-file", LOG_FILE_ALICE]
    capture(command)

    # Alice sees "alice_server.log" file in the "logs" directory.
    assert os.path.exists(LOG_FILE_ALICE)


# Alice notices that her log file does not contain debug messages.
# She knows from the help message default logging level is INFO.
@clean_up
def test_main_log_file_contains_debug():
    # Alice decides to set logging level to DEBUG using "--log-level DEBUG" option.
    command = [PYTHON_EXE, "main.py", "-d", DATA_DIR, "--log-file", LOG_FILE_ALICE, "--log-level", "DEBUG"]
    capture(command)

    # After running the app, Alice sees that her log file now contains debug messages.
    with open(LOG_FILE_ALICE, "r") as logfile:
        log = logfile.read()
    assert "DEBUG" in log


# Satisfied Alice takes a cup of coffee and relax.
