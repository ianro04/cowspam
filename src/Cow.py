from __future__ import annotations

from dataclasses import dataclass, field
import random

import cowsay

COWSAY_CHARS = [
    character
    for character in cowsay.char_names
    if character not in ["cow", "beavis", "ghostbusters", "miki", "stimpy"]
]


@dataclass
class Cow:
    name: str = "Unnamed Cow"
    age: int | None = None
    is_normal_cow: bool | None = None
    _rare_char: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.age = self.age if self.age is not None else round(random.triangular(0, 20, 4))
        if self.is_normal_cow is None:
            normal_chance = 0.70 if self.age <= 2 else 0.99
            self.is_normal_cow = random.random() < normal_chance
        self._rare_char = None if self.is_normal_cow else random.choice(COWSAY_CHARS)

    @property
    def _char(self) -> str | None:
        return "cow" if self.is_normal_cow else self._rare_char

    @property
    def _title(self) -> str:
        if "Cow" in self.name:
            return self.name
        return f"{self.name} the Cow" if self.is_normal_cow else f"{self.name} the {self._rare_char}?"

    def _render(self, message: str, signature: str) -> str:
        return cowsay.get_output_string(self._char, f"{message}\n-{signature}")

    def moo_text(self) -> str:
        if self.is_normal_cow:
            return self._render("Moo!", f"{self.name}, age {self.age}")
        return self._render("Moo?", self._title)  # Nothing to see here

    def speak_text(self, message: str) -> str:
        return self._render(message, self._title)

    def moo(self) -> None:
        print(self.moo_text())

    def speak(self, message: str) -> None:
        print(self.speak_text(message))
