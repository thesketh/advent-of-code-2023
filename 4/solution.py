"""Solution to the fourth advent of code problem."""
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""

ScratchcardID = int
"""The ID of the scratchcard."""


@dataclass
class Scratchcard:
    """A scratchcard."""

    number: ScratchcardID
    """The number of the scratchcard."""
    winning_numbers: set[int]
    """The set of winning numbers."""
    drawn_numbers: set[int]
    """The set of drawn numbers."""

    @property
    def n_matching_numbers(self) -> int:
        return len(self.drawn_numbers & self.winning_numbers)

    def score(self) -> int:
        n_matching_numbers = self.n_matching_numbers
        if not n_matching_numbers:
            return 0
        return 2 ** (n_matching_numbers - 1)


def load_data() -> list[Scratchcard]:
    """Load the relevant data from the scratchcards."""
    scratchcards = []

    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line in map(str.rstrip, file):
            card_info, numbers = line.split(": ", 1)
            winning_numbers_str, drawn_numbers_str = numbers.split(" | ", 1)

            card_number = int(card_info.split(" ", 1)[-1])
            winning_numbers = set(map(int, winning_numbers_str.split()))
            drawn_numbers = set(map(int, drawn_numbers_str.split()))

            scratchcards.append(
                Scratchcard(card_number, winning_numbers, drawn_numbers)
            )

    return scratchcards


def calculate_score(scratchcards: list[Scratchcard]) -> int:
    """Calculate the sum of the scores from the scratchcards."""
    return sum(scratchcard.score() for scratchcard in scratchcards)


def count_scratchcards(scratchcards: list[Scratchcard]) -> int:
    """Count the number of scratchcards evaluated according to the rules."""
    n_scratchcards = 0

    extra_copies: Counter[ScratchcardID] = Counter()
    for scratchcard in scratchcards:
        scratchcard_number = scratchcard.number
        n_cards = 1 + extra_copies[scratchcard_number]

        n_matching_numbers = scratchcard.n_matching_numbers
        for n in range(1, n_matching_numbers + 1):
            extra_copies[scratchcard_number + n] += n_cards

        n_scratchcards += n_cards

    return n_scratchcards


def main():
    """Run the advent of code solution."""
    scratchcards = load_data()
    print("Scratchcard score sum:", calculate_score(scratchcards))
    print("Total scratchcards evaluated:", count_scratchcards(scratchcards))


if __name__ == "__main__":
    main()
