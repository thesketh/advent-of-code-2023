"""Solution to the third advent of code problem."""
import re
from dataclasses import dataclass
from itertools import chain
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""


@dataclass
class Number:
    """A number in the engine schematic."""

    start_index: int
    end_index: int
    value: int


@dataclass
class Symbol:
    """A symbol in the engine schematic."""

    index: int
    value: str


def load_data() -> tuple[list[list[Number]], list[list[Symbol]]]:
    """
    Load the relevant data from the engine schematic, parsing the numbers
    and symbols on each line.

    """
    all_numbers, all_symbols = [], []

    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line in map(str.rstrip, file):
            line_numbers = []
            line_symbols = []

            for number_match in re.finditer(r"[0-9]+", line):
                value = int(number_match.group(0))
                span = number_match.span()

                number = Number(start_index=span[0], end_index=span[1] - 1, value=value)
                line_numbers.append(number)

            for symbol_match in re.finditer(r"[^0-9\.]", line):
                symbol = Symbol(symbol_match.start(), symbol_match.group(0))
                line_symbols.append(symbol)

            all_numbers.append(line_numbers)
            all_symbols.append(line_symbols)

    return all_numbers, all_symbols


def calculate_part_number_sum(
    numbers: list[list[Number]], symbols: list[list[Symbol]]
) -> int:
    """Calculate the sum of the part numbers."""
    total = 0

    for line_index, number_line in enumerate(numbers):
        symbols_before = [] if line_index == 0 else symbols[line_index - 1]
        symbols_current = symbols[line_index]
        symbols_after = (
            [] if line_index == (len(numbers) - 1) else symbols[line_index + 1]
        )

        for number in number_line:
            for symbol in chain(symbols_before, symbols_current, symbols_after):
                if (number.start_index - 1) <= symbol.index <= (number.end_index + 1):
                    total += number.value
                    break

    return total


def calculate_gear_ratio_sum(
    numbers: list[list[Number]], symbols: list[list[Symbol]]
) -> int:
    """Calculate the sum of the gear ratios for the gears in the schematic."""
    total = 0

    for line_index, symbol_line in enumerate(symbols):
        numbers_before = [] if line_index == 0 else numbers[line_index - 1]
        numbers_current = numbers[line_index]
        numbers_after = (
            [] if line_index == (len(symbols) - 1) else numbers[line_index + 1]
        )

        for symbol in symbol_line:
            if symbol.value != "*":
                continue

            gear_values = []
            for number in chain(numbers_before, numbers_current, numbers_after):
                if (number.start_index - 1) <= symbol.index <= (number.end_index + 1):
                    gear_values.append(number.value)
            if len(gear_values) == 2:
                total += gear_values[0] * gear_values[1]

    return total


def main():
    """Run the advent of code solution."""
    numbers, symbols = load_data()
    print("Part number sum:", calculate_part_number_sum(numbers, symbols))
    print("Gear ratio sum:", calculate_gear_ratio_sum(numbers, symbols))


if __name__ == "__main__":
    main()
