#!/usr/bin/env python3
"""tests for article.py"""

import os
import sys
import random
from subprocess import getstatusoutput

# The script/program under test
prg = './article.py'

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
def test_masculine_lower():
    """masculine_lower"""

    word = random.choice('chico teatro cartero'.split())
    rv, out = getstatusoutput(f'{PYTHON} {prg} {word}')
    assert rv == 0
    assert out == f'Me gusto el {word}.'


# --------------------------------------------------
def test_masculine_upper():
    """masculine_upper"""

    word = random.choice('CHICO TEATRO CARTERO'.split())
    rv, out = getstatusoutput(f'{PYTHON} {prg} {word}')
    assert rv == 0
    assert out == f'Me gusto el {word}.'


# --------------------------------------------------
def test_feminine_lower():
    """feminine_lower"""

    word = random.choice('chica gata abuela'.split())
    rv, out = getstatusoutput(f'{PYTHON} {prg} {word}')
    assert rv == 0
    assert out == f'Me gusto la {word}.'


# --------------------------------------------------
def test_feminine_upper():
    """feminine_upper"""

    word = random.choice('CHICA GATA ABUELA'.split())
    rv, out = getstatusoutput(f'{PYTHON} {prg} {word}')
    assert rv == 0
    assert out == f'Me gusto la {word}.'
