"""Public API for the cowspam library."""

from .Cow import COWSAY_CHARS, Cow
from .cli import clear_screen, main, print_tally
from .generator import make_cow_text, run_kilobytes

__all__ = [
    "COWSAY_CHARS",
    "Cow",
    "clear_screen",
    "main",
    "make_cow_text",
    "print_tally",
    "run_kilobytes",
]
