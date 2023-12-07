"""Solution to the second advent of code problem."""
from collections import Counter
from math import prod
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""

GameID = int
"""The ID of a game played by the elf."""
CubeColour = str
"""A cube colour used in the game."""
MaxCubeCount = int
"""The maximum number of times the colour was drawn in a game."""
Game = dict[CubeColour, MaxCubeCount]
"""The results of a specific game (the maximum count for each colour)."""
Games = dict[GameID, Game]
"""Information about the games played."""


def load_data() -> Games:
    """Load the relevant data."""
    games: Games = {}
    with DATA_PATH.open("r", encoding="utf-8") as file:
        for line in map(str.rstrip, file):
            if not line:
                continue
            game: Game = Counter()

            game_id_string, game_results = line.split(": ", 1)
            game_id = int(game_id_string.split(" ", 1)[-1])

            for round_result in game_results.split("; "):
                for colour_result in round_result.split(", "):
                    count_str, colour = colour_result.split(" ", 1)
                    count = int(count_str)

                    if game[colour] < count:
                        game[colour] = count

            games[game_id] = game
    return games


def calculate_sum_of_ids(data: Games) -> int:
    """Calculate the sum of the IDs of games where counts meet certain criteria."""
    total = 0
    for game_id, max_counts in data.items():
        if max_counts["red"] > 12:
            continue
        if max_counts["green"] > 13:
            continue
        if max_counts["blue"] > 14:
            continue
        total += game_id
    return total


def calculate_sum_of_powers(data: Games) -> int:
    """Calculate the sum of the powers of the cubes."""
    return sum(map(lambda counts: prod(counts.values()), data.values()))


def main():
    """Run the advent of code solution."""
    part_1_data = load_data()
    print("Sum of IDs:", calculate_sum_of_ids(part_1_data))
    print("Sum of powers:", calculate_sum_of_powers(part_1_data))


if __name__ == "__main__":
    main()
