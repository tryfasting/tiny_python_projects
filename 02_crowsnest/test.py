#!/usr/bin/env python3
"""tests for crowsnest.py"""

import os
import sys
from subprocess import getstatusoutput, getoutput

# The script/program under test
prg = './crowsnest.py'

# Path to the Python interpreter in the current virtual environment
PYTHON = sys.executable
consonant_words = [
    'brigantine', 'clipper', 'dreadnought', 'frigate', 'galleon', 'haddock',
    'junk', 'ketch', 'longboat', 'mullet', 'narwhal', 'porpoise', 'quay',
    'regatta', 'submarine', 'tanker', 'vessel', 'whale', 'xebec', 'yatch',
    'zebrafish'
]
vowel_words = ['aviso', 'eel', 'iceberg', 'octopus', 'upbound']
template = 'Ahoy, Captain, {} {} off the larboard bow!'


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
def test_consonant():
    """brigantine -> a brigantine"""

    for word in consonant_words:
        out = getoutput(f'{PYTHON} {prg} {word}')
        assert out.strip() == template.format('a', word)


# --------------------------------------------------
def test_consonant_upper():
    """brigantine -> a Brigatine"""

    for word in consonant_words:
        out = getoutput(f'{PYTHON} {prg} {word.title()}')
        assert out.strip() == template.format('a', word.title())


# --------------------------------------------------
def test_vowel():
    """octopus -> an octopus"""

    for word in vowel_words:
        out = getoutput(f'{PYTHON} {prg} {word}')
        assert out.strip() == template.format('an', word)


# --------------------------------------------------
def test_vowel_upper():
    """octopus -> an Octopus"""

    for word in vowel_words:
        out = getoutput(f'{PYTHON} {prg} {word.upper()}')
        assert out.strip() == template.format('an', word.upper())
