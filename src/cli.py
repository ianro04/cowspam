from __future__ import annotations

import argparse
import os
import sys
import time
from collections import Counter
from subprocess import run as srun

from faker import Faker

from .Cow import Cow
from .generator import run_kilobytes


def clear_screen() -> None:
    command = "cls" if os.name == "nt" else "clear"
    srun(command, shell=True)


def print_tally(counter: Counter[str], file=None) -> None:
    total = sum(counter.values())
    print("\n ☆ FINAL TALLY ☆ ", file=file)
    for item, count in counter.most_common():
        percent = (count / total) * 100 if total else 0
        print(f"{item}: {count} ({percent:.2f}%)", file=file)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Flood your terminal/output with random cows that moo (most of the time)."
    )
    parser.add_argument(
        "-a",
        "--auto",
        action="store_true",
        help="Run without the 1-second delay between cows",
    )
    parser.add_argument(
        "-f",
        "--flash",
        action="store_true",
        help="Clear the screen for each cow, creating a flashing effect",
    )
    parser.add_argument(
        "loops",
        nargs="?",
        type=int,
        default=100,
        help="Number of cows to generate (default: 100)",
    )
    parser.add_argument(
        "-k",
        "--kb",
        "--kilobytes",
        dest="kilobytes",
        metavar="KB",
        type=int,
        help=(
            "Kilobytes of cows to generate (overrides loops). "
            "Output is written if stdout is piped/redirected, otherwise discarded."
        ),
    )
    parser.add_argument(
        "-n",
        "--normal",
        action="store_true",
        help="Only generate normal cows",
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
        counter, produced = run_kilobytes(
            args.kilobytes,
            write_output=not stdout_is_tty,
            normal_only=args.normal,
        )
        print_tally(counter, file=sys.stderr)
        print(
            f"Generated ~{produced / 1024:.2f} KB of cows"
            f"{' (discarded; redirect stdout to keep them)' if stdout_is_tty else ''}",
            file=sys.stderr,
        )
        return 0

    cow_counter: Counter[str] = Counter()
    fake = Faker()
    for _ in range(args.loops):
        if not auto:
            time.sleep(1)
        cow = Cow(
            fake.first_name_female(),
            is_normal_cow=True if args.normal else None,
        )
        if flash:
            clear_screen()
        cow.moo()
        cow_counter.update(
            ["Normal Cows" if cow.is_normal_cow else "Anomalous Cows"]
        )

    print_tally(cow_counter)
    return 0
