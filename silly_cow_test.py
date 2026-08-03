import argparse
import cowsay
import random
import time
from collections import Counter
from faker import Faker

# Purpose: Bovine terminal spam

class Cow:
    def __init__(self, name=""):
        self.name = name or "Unnamed Cow"
        self.age = round(random.triangular(0, 20, 4))
        normal_chance = 0.70 if self.age <= 2 else 0.99
        if random.random() >= normal_chance:
            self.is_normal_cow = False
            self._rare_char = random.choice([x for x in cowsay.char_names if x not in ['cow', 'beavis', 'ghostbusters', 'miki', 'stimpy']])
        else:
            self.is_normal_cow = True
            self._rare_char = None

    def moo(self):
        def _moo_rare():
            char_moo = getattr(cowsay, self._rare_char)
            char_moo(f"Moo?\n-{self.name} the {self._rare_char}?")
	    
        if not self.is_normal_cow:
            _moo_rare() # Nothing to see here
        else:
        	cowsay.cow(f"Moo!\n-{self.name}, age {self.age}")

    def speak(self, message):
        if not self.is_normal_cow:
            char_speak = getattr(cowsay, self._rare_char)
            char_speak(f"{message}\n-{self.name} the {self._rare_char}?")
        else:
            cowsay.cow(f"{message}\n-{self.name} the Cow")

    def __str__(self):
        if not self.is_normal_cow:
            return f"{self.name} the {self._rare_char}?, age {self.age}"
        else:
            return f"{self.name} the Cow, age {self.age}"

def main():
    parser = argparse.ArgumentParser(
        description="Flood your terminal/output with random cows that moo (most of the time)."
    )
    parser.add_argument(
        "-a", "--auto",
        action="store_true",
        help="Run without the 1-second delay between cows"
    )
    parser.add_argument(
        "loops",
        nargs="?",
        type=int,
        default=100,
        help="Number of cows to generate (default: 100)"
    )
    args = parser.parse_args()

    if args.loops < 1:
        parser.error("Loops must be a positive integer.")

    c_counter = Counter()

    fake = Faker()
    for _ in range(args.loops):
        if not args.auto:
            time.sleep(1)
        c = Cow(fake.first_name_female())
        c.moo()
        c_counter.update(["Anomalous Cows" if not(c.is_normal_cow) else "Normal Cows"])

    print("\n ☆ FINAL TALLY ☆ ")
    if c_counter["Anomalous Cows"] == 0:
        c_counter["Cows"] = c_counter.pop("Normal Cows")
    for item, count in c_counter.most_common():
        percent = (count / args.loops) * 100
        print(f"{item}: {count} ({percent:.2f}%)")

if __name__ == "__main__":
    main()

