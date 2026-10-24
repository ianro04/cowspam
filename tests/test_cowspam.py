import os
import sys

import cowsay
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from silly_cow_test import Cow

def test_cow_init():
    cow = Cow(name="Bessie")
    assert cow.name == "Bessie"
    assert isinstance(cow.age, int)
    assert isinstance(cow.is_normal_cow, bool)
    if not cow.is_normal_cow:
        assert cow._rare_char in [x for x in cowsay.char_names if x not in ['cow', 'beavis', 'ghostbusters', 'miki', 'stimpy']]
    else:
        assert cow._rare_char is None

def test_moo():
    c = Cow()
    try:
        c.moo()
    except Exception as e:
        pytest.fail(f"moo() raised an exception: {e}")

