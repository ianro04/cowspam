# Purpose: Bovine terminal spam
from __future__ import annotations

import argparse
import os
import random
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from subprocess import run as srun

import cowsay
from faker import Faker

KB_BATCH_SIZE = 64

@dataclass
class Cow:
    name: str = "Unnamed Cow"
    age: int = None
    is_normal_cow: bool = field(init=False)
    _rare_char: str | None = field(init=False, default=None)

    def __post_init__(self):
        self.age = self.age if self.age is not None else round(random.triangular(0, 20, 4))
        normal_chance = 0.70 if self.age <= 2 else 0.99
        if random.random() >= normal_chance:
            self.is_normal_cow = False
            self._rare_char = random.choice([x for x in cowsay.char_names if x not in ['cow', 'beavis', 'ghostbusters', 'miki', 'stimpy']])
        else:
            self.is_normal_cow = True
            self._rare_char = None

    @property
    def _char(self):
        return "cow" if self.is_normal_cow else self._rare_char

    @property
    def _title(self):
        return f"{self.name} the Cow" if self.is_normal_cow else f"{self.name} the {self._rare_char}?"

    def _render(self, message, signature):
        return cowsay.get_output_string(self._char, f"{message}\n-{signature}")

    def moo_text(self):
        if self.is_normal_cow:
            return self._render("Moo!", f"{self.name}, age {self.age}")
        return self._render("Moo?", self._title)  # Nothing to see here

    def speak_text(self, message):
        return self._render(message, self._title)

    def moo(self):
        print(self.moo_text())

    def speak(self, message):
        print(self.speak_text(message))

    def __str__(self):
        return f"{self._title}, age {self.age}"

_thread_local = threading.local()

def _get_faker():
    if not hasattr(_thread_local, "fake"):
        _thread_local.fake = Faker()
    return _thread_local.fake

def make_cow_text():
    """Build one random cow. Returns (rendered_text, is_normal_cow)."""
    cow = Cow(_get_faker().first_name_female())
    return cow.moo_text(), cow.is_normal_cow

def clear_screen():
    command = ('cls' if os.name == 'nt' else 'clear')
    srun(command, shell=True)

def print_tally(counter, file=None):
    total = sum(counter.values())
    print("\n ☆ FINAL TALLY ☆ ", file=file)
    for item, count in counter.most_common():
        percent = (count / total) * 100 if total else 0
        print(f"{item}: {count} ({percent:.2f}%)", file=file)

def run_kilobytes(kilobytes, write_output):
    """Generate cows in a thread pool until at least `kilobytes` KB have been produced."""
    target = kilobytes * 1024
    produced = 0
    counter = Counter()

    with ThreadPoolExecutor() as pool:
        while produced < target:
            for text, is_normal in pool.map(lambda _: make_cow_text(), range(KB_BATCH_SIZE)):
                if write_output:
                    sys.stdout.write(text + "\n")
                produced += len(text.encode("utf-8")) + 1
                counter.update(["Normal Cows" if is_normal else "Anomalous Cows"])
                if produced >= target:
                    break

    return counter, produced

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Flood your terminal/output with random cows that moo (most of the time)."
    )
    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        help="Run without the 1-second delay between cows"
    )
    parser.add_argument(
        "-f", "--flash",
        action="store_true",
        help="Clear the screen for each cow, creating a flashing effect"
    )
    parser.add_argument(
        "loops",
        nargs="?",
        type=int,
        default=100,
        help="Number of cows to generate (default: 100)"
    )
    parser.add_argument(
        "-k", "--kb", "--kilobytes",
        dest="kilobytes",
        metavar="KB",
        type=int,
        help="Kilobytes of cows to generate (overrides loops). "
             "Output is written if stdout is piped/redirected, otherwise discarded."
    )
    args = parser.parse_args()

    stdout_is_tty = sys.stdout.isatty()
    piped = not sys.stdin.isatty() or not stdout_is_tty

    if args.loops < 1:
        parser.error("Loops must be a positive integer.")
    if args.kilobytes is not None and args.kilobytes < 1:
        parser.error("Kilobytes must be a positive integer.")

    flash = args.flash and stdout_is_tty
    auto = args.auto or piped

    if args.kilobytes is not None:
        counter, produced = run_kilobytes(args.kilobytes, write_output=not stdout_is_tty)
        print_tally(counter, file=sys.stderr)
        print(f"Generated ~{produced / 1024:.2f} KB of cows"
              f"{' (discarded; redirect stdout to keep them)' if stdout_is_tty else ''}",
              file=sys.stderr)
        return 0

    c_counter = Counter()
    fake = Faker()
    for _ in range(args.loops):
        if not auto:
            time.sleep(1)
        c = Cow(fake.first_name_female())
        if flash:
            clear_screen()
        c.moo()
        c_counter.update(["Anomalous Cows" if not c.is_normal_cow else "Normal Cows"])

    print_tally(c_counter)
    return 0

if __name__ == "__main__":
    sys.exit(main())