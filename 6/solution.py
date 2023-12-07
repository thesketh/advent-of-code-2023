"""Solution to the sixth advent of code problem."""
import re
from dataclasses import dataclass
from math import prod
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""


@dataclass
class RaceRecord:
    time: int
    distance: int

    def count_ways_to_beat(self) -> int:
        """Count the number of ways to beat the record."""
        # Could do a binary search here, but naive fast enough.
        total = 0
        for speed in range(1, self.time):
            if (speed * (self.time - speed)) > self.distance:
                total += 1
        return total


def load_data() -> list[RaceRecord]:
    """Load the relevant data from the race records."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        lines = map(str.rstrip, file)
        times_line = next(lines)
        distances_line = next(lines)

        pattern = re.compile("[0-9]+")
        times = map(int, pattern.findall(times_line))
        distances = map(int, pattern.findall(distances_line))
        return [RaceRecord(time, distance) for time, distance in zip(times, distances)]


def product_of_ways_to_beat_record(race_records: list[RaceRecord]):
    """Return the product of the number of ways to beat the record for each race."""
    return prod([race_record.count_ways_to_beat() for race_record in race_records])


def count_ways_to_beat_record_in_long_race(race_records: list[RaceRecord]):
    """Return the number of ways to beat the record in a long race."""
    times, distances = [], []
    for race_record in race_records:
        times.append(race_record.time)
        distances.append(race_record.distance)
    long_time = int("".join(map(str, times)))
    long_distance = int("".join(map(str, distances)))

    return RaceRecord(long_time, long_distance).count_ways_to_beat()


def main():
    """Run the advent of code solution."""
    race_records = load_data()
    print("Ways to beat record:", product_of_ways_to_beat_record(race_records))
    race_records = load_data()
    print(
        "Ways to beat record in long race:",
        count_ways_to_beat_record_in_long_race(race_records),
    )


if __name__ == "__main__":
    main()
