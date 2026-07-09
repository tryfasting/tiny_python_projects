#!/usr/bin/env python3
"""tests for hello.py"""

import os
import sys
from subprocess import getstatusoutput, getoutput

# The script/program under test
prg = './hello.py'

# Path to the Python interpreter in the current virtual environment
PYTHON = sys.executable


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_runnable():
    """Runs using python3"""

    out = getoutput(f'python3 {prg}')
    assert out.strip() == 'Hello, World!'


# --------------------------------------------------
def test_executable():
    """Says 'Hello, World!' by default"""

    out = getoutput(f'{PYTHON} {prg}')
    assert out.strip() == 'Hello, World!'


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PYTHON} {prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_input():
    """test for input"""

    for val in ['Universe', 'Multiverse']:
        for option in ['-n', '--name']:
            rv, out = getstatusoutput(f'{PYTHON} {prg} {option} {val}')
            assert rv == 0
            assert out.strip() == f'Hello, {val}!'
