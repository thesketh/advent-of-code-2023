"""Solution to the first advent of code problem."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""

DigitChar = str
"""A single numeric character."""

WRITTEN_NUMBER_REPLACEMENTS: dict[str, DigitChar] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
"""
A string to string mapping containing written numbers and the numerical
characters they should be replaced with.

"""
WRITTEN_NUMBER_REGEX = "|".join(WRITTEN_NUMBER_REPLACEMENTS.keys())
"""Regex to match a written number."""
NUMERIC_OR_WRITTEN_REGEX = f"(?=([0-9]|{WRITTEN_NUMBER_REGEX}))"
"""
A regex pattern for a single numeric digit (including written numbers).

This matches overlapping numbers (e.g. 'nineight' unpacks to ['nine', 'eight']).

"""


def load_data(parse_written_numbers: bool = False) -> list[list[DigitChar]]:
    """Load the relevant data."""
    lines = []
    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.rstrip()
            if not line:
                continue

            if not parse_written_numbers:
                line_digits: list[str] = list(filter(str.isnumeric, line))
            else:
                line_digits = list(
                    re.findall(NUMERIC_OR_WRITTEN_REGEX, line)
                )
                for index, digit in enumerate(line_digits):
                    if digit.isnumeric():
                        continue
                    line_digits[index] = WRITTEN_NUMBER_REPLACEMENTS[digit]
                if not line_digits:
                    print(line)

            lines.append(line_digits)
    return lines


def calculate_calibration_value(data: list[list[DigitChar]]) -> int:
    """Calculate the numeric calibration value."""
    return sum(int(line[0] + line[-1]) for line in data)


def main():
    """Run the advent of code solution."""
    part_1_data = load_data()
    print("Calibration value:", calculate_calibration_value(part_1_data))
    part_2_data = load_data(parse_written_numbers=True)
    print(
        "Calibration value when parsing written numbers:",
        calculate_calibration_value(part_2_data),
    )


if __name__ == "__main__":
    main()
