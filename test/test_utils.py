# test/test_utils.py
import sys
import os

# Get the parent directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')

# Add the parent directory to the sys.path list
sys.path.append(parent_dir)
from utils import sumvalues, maxvalue, minvalue, meanvalue, countvalue

def test_sumvalues():
    assert sumvalues([1, 2, 3]) == 6
    assert sumvalues([-1, 0, 1]) == 0
    assert sumvalues([]) == 0

def test_maxvalue():
    assert maxvalue([1, 5, 3]) == 5
    assert maxvalue([-1, 0, 1]) == -1

def test_minvalue():
    assert minvalue([1, 5, 3]) == 1
    assert minvalue([-1, 0, 1]) == -1

def test_meanvalue():
    assert meanvalue([1, 2, 3]) == 2.0
    assert meanvalue([-1, 0, 1]) == 0.0

def test_countvalue():
    assert countvalue([1, 2, 2, 3, 3, 3], 2) == 2
    assert countvalue([1, 2, 2, 3, 3, 3], 4) == 0
