#!/usr/bin/env python3
"""tests for jump.py"""

import os
import sys
from subprocess import getstatusoutput

# The script/program under test
prg = './jump.py'

# Path to the Python interpreter in the current virtual environment
PYTHON = sys.executable


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PYTHON} {prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_01():
    """test"""

    rv, out = getstatusoutput(f'{PYTHON} {prg} 123-456-7890')
    assert rv == 0
    assert out == '987-604-3215'


# --------------------------------------------------
def test_02():
    """test"""

    rv, out = getstatusoutput(f'{PYTHON} {prg} "That number to call is 098-765-4321."')
    assert rv == 0
    assert out.rstrip() == 'That number to call is 512-340-6789.'
