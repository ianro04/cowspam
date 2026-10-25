import os
import sys

import cowsay
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cowspam import (Cow, COWSAY_CHARS, run_kilobytes)

def test_cow_init():
    cow = Cow(name="Bessie")
    assert cow.name == "Bessie"
    assert isinstance(cow.age, int)
    assert isinstance(cow.is_normal_cow, bool)
    if not cow.is_normal_cow:
        assert cow._rare_char in COWSAY_CHARS
    else:
        assert cow._rare_char is None

def test_moo():
    c = Cow()
    try:
        c.moo()
    except Exception as e:
        pytest.fail(f"moo() raised an exception: {e}")

def test_cow_speak():
    c = Cow()
    try:
        c.speak("Hello, world!")
    except Exception as e:
        pytest.fail(f"speak() raised an exception: {e}")

def test_cow_str():
    c = Cow(name="Betsy", age=5)
    expected_str = f"{c._title}, age {c.age}"
    assert str(c) == expected_str

def test_kb_produced_small():
    (output_counter, output_kb) = run_kilobytes(1, False)
    assert output_counter.total() <= 5
    assert output_kb >= 1024

def test_kb_produced_large():
    (output_counter, output_kb) = run_kilobytes(2000, False) # 2 MB
    assert output_counter.total() <= 7000
    assert output_kb >= 10240

def test_rare_moo():
    c = Cow()
    while c.is_normal_cow:
        c = Cow()
    try:
        c.moo()
        assert c.moo_text() == c._render("Moo?", c._title)
    except Exception as e:
        pytest.fail(f"moo() raised an exception for rare cow: {e}")
