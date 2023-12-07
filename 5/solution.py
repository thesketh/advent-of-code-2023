"""Solution to the fifth advent of code problem."""
from bisect import insort
from collections import deque
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""


Seeds = list[int]
"""A list of the seeds in an almanac."""
Offset = int
"""An offset between two ranges of numbers."""


class OffsetMapping:
    """
    A mapping which maps numbers within a range to numbers within another,
    storing input ranges with an offset.

    Number ranges without an offset will be treated as though they have an
    offset of 0.

    """

    def __init__(
        self, data: list[tuple[range, Offset]] | None = None, /, name: str | None = None
    ) -> None:
        self.name = name
        """The name of the mapping."""
        self._offsets: deque[tuple[range, Offset]] = deque()
        """The offsets for each input range."""

        if data:
            for key, value in data:
                self[key] = value

    def __repr__(self) -> str:
        name = f"name={self.name!r}; " if self.name else ""
        offsets = ", ".join(
            [f"{repr(key)}: {repr(value)}" for key, value in self._offsets]
        )
        return f"{self.__class__.__name__}({name}{{{offsets}}})"

    def __setitem__(self, key: range, value: Offset):
        """Add a range to the mapping."""
        if not key.step == 1:
            raise ValueError("Range step must be 1")

        insort(
            self._offsets, (key, value), key=lambda item: (item[0].start, item[0].stop)
        )

    def __getitem__(self, key: int) -> int:
        """Get the offset value from the stored ranges."""
        for source_range, offset in self._offsets:
            if source_range.start > key:
                break
            if key in source_range:
                return key + offset
        return key

    def get_ranges(self, input_ranges: list[range]) -> list[range]:
        """Get the mapped ranges from a sequence of input ranges."""
        range_queue: deque[range] = deque()
        for input_range in sorted(input_ranges, key=lambda rng: (rng.start, rng.stop)):
            if input_range.step != 1:
                raise ValueError("All input ranges must have step 1")
            range_queue.append(input_range)

        output_ranges = []
        while range_queue:
            input_range = range_queue.popleft()
            has_mapped_range = True

            for source_range, offset in self._offsets:
                if source_range.start > input_range.stop:
                    # Source ranges are sorted, so can assume no overlap
                    # for following ranges.
                    has_mapped_range = False
                    break

                overlap = range(
                    max(input_range.start, source_range.start),
                    min(input_range.stop, source_range.stop),
                )
                if not overlap:
                    continue

                uncovered_start = None
                uncovered_end = None
                if input_range.start < overlap.start:
                    uncovered_start = range(input_range.start, overlap.start)
                if input_range.stop > overlap.stop:
                    uncovered_end = range(overlap.stop, input_range.stop)

                overlap_output = range(overlap.start + offset, overlap.stop + offset)
                output_ranges.append(overlap_output)

                if uncovered_start or uncovered_end:
                    if uncovered_end:
                        range_queue.appendleft(uncovered_end)
                    if uncovered_start:
                        range_queue.appendleft(uncovered_start)
                break
            else:
                has_mapped_range = False

            if not has_mapped_range:
                output_ranges.append(input_range)

        return output_ranges


def load_data() -> tuple[Seeds, Sequence[OffsetMapping]]:
    """Load the relevant data from the almanac."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        lines = map(str.rstrip, file)

        seeds_line = next(lines)
        seeds = list(map(int, seeds_line.split(": ", 1)[-1].split()))
        next(lines)  # Skip the empty line.

        offset_mappings = []
        while True:
            try:
                map_definition = next(lines)
            except StopIteration:
                break
            if not map_definition:
                break
            offset_mapping = OffsetMapping(name=map_definition.split(" ")[0])

            for line in iter(lines.__next__, ""):
                target_start, source_start, length = map(int, line.split(" ", 3))
                source_range = range(source_start, source_start + length)
                offset = target_start - source_start
                offset_mapping[source_range] = offset

            offset_mappings.append(offset_mapping)

    return seeds, offset_mappings


def get_lowest_location_number(
    seeds: Seeds, offset_mappings: Sequence[OffsetMapping]
) -> int:
    """Get the lowest location number from the seeds."""
    location_numbers = []

    for seed in seeds:
        location_number = seed
        for mapping in offset_mappings:
            location_number = mapping[location_number]
        location_numbers.append(location_number)

    return min(location_numbers)


def get_lowest_location_number_from_ranges(
    seeds: Seeds, offset_mappings: Sequence[OffsetMapping]
) -> int:
    """Get the lowest location number from the seed ranges."""
    iterator = iter(seeds)
    seed_ranges = []
    for range_start, range_length in zip(iterator, iterator):
        seed_ranges.append(range(range_start, range_start + range_length))

    location_numbers = []
    for seed_range in seed_ranges:
        output_ranges = [seed_range]
        for mapping in offset_mappings:
            output_ranges = mapping.get_ranges(output_ranges)
        location_numbers.append(min(range_.start for range_ in output_ranges))

    return min(location_numbers)


def main():
    """Run the advent of code solution."""
    seeds, offset_mappings = load_data()
    print("Lowest location number:", get_lowest_location_number(seeds, offset_mappings))
    print(
        "Lowest location number from seed range:",
        get_lowest_location_number_from_ranges(seeds, offset_mappings),
    )


if __name__ == "__main__":
    main()
