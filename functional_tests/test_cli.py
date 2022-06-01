"""Functional tests for CLI

Imports:
    os
    subprocess
"""

import os
import platform
import subprocess

DATA_DIR = "data"
EXECUTION_TIMEOUT = 5
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


# Alice has heard about a new cool file server app.
# She downloaded the package from its homepage into a local directory.


def test_main_no_param():
    # Since Alice is an experienced user she immediately runs the main module from CLI.
    command = [PYTHON_EXE, "main.py"]
    out, err, exitcode = capture(command)

    # Alice notices an error message about some required arguments.
    assert exitcode == 0
    assert b"Run error!" in out
    assert b"error: the following arguments are required: -d/--data-directory" in err


def test_main_help_param():
    # To understand what arguments the main module gets, she runs the main module with "-h" argument.
    command = [PYTHON_EXE, "main.py", "-h"]
    out, err, exitcode = capture(command)

    # Alice notices an error message about some required arguments.
    assert exitcode == 0
    assert b"usage:" in out
    assert err == b""


# Now Alice knows that she must provide a location of the data directory.


def test_main_datadir_param():
    # So, Alice starts the app with a required argument "-d".
    command = [PYTHON_EXE, "main.py", "-d", DATA_DIR]
    out, err, exitcode = capture(command)

    # And sees that now app starts without errors.
    assert exitcode == 0
    assert out == b""
    assert err == b""

    # Also Alice notices that specified data directory is exists now
    assert os.path.exists(DATA_DIR)


# Alice is also a very curious person. She wants to try an alternative argument for specifying data directory.


def test_main_datadiralt_param():
    # Firstly, Alice removes freshly created data directory to check if it will be created again.
    if os.path.exists(DATA_DIR):
        os.rmdir(DATA_DIR)

    # She starts the app again using "--data-directory" to specify the data directory.
    command = [PYTHON_EXE, "main.py", "--data-directory", "data"]
    out, err, exitcode = capture(command)

    # Again, Alice sees that the app starts without errors.
    assert exitcode == 0
    assert out == b""
    assert err == b""

    # And she notices that specified data directory was created once more time
    assert os.path.exists(DATA_DIR)


# Satisfied Alice takes a cup of coffee and relax.
