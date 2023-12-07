"""Solution to the seventh advent of code problem."""
from collections import Counter
from pathlib import Path
from typing import Literal, get_args

ROOT = Path(__file__).parent
"""Root of the solution."""
DATA_PATH = ROOT.joinpath("data.txt")
"""Path to the data input file."""

Card = Literal["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
"""A string representing a card."""
Value = int
"""The value of a card. For a numeric card, the number."""
Bet = int
"""The value of a bet."""
HandRank = int
"""The rank of a hand (higher is better)."""


CARD_VALUES: dict[Card, Value] = {
    card: score for score, card in enumerate(get_args(Card), 2)
}
"""The values of each card."""
CARD_VALUES_WITH_JOKERS = CARD_VALUES.copy()
"""The values of each card when J is a joker."""
CARD_VALUES_WITH_JOKERS["J"] = 0


class Hand:
    """A hand in camel cards."""

    def __init__(self, cards: list[Card], bet: Bet):
        self.cards = cards
        """The cards in the hand."""
        self.bet = bet
        """The bet for the hand."""

    def get_card_values(self, j_is_joker: bool = False) -> tuple[Value, ...]:
        """Get the values of the cards, in order."""
        if j_is_joker:
            card_values = CARD_VALUES_WITH_JOKERS
        else:
            card_values = CARD_VALUES
        return tuple(card_values[card] for card in self.cards)

    def get_rank(self, j_is_joker: bool = False) -> HandRank:
        """Get the rank for the hand (higher is better)."""
        counter = Counter(self.cards)
        if j_is_joker:
            n_jokers = counter.pop("J", 0)
            if n_jokers == 5:
                most_common_card: Card = "J"
            else:
                most_common_card = counter.most_common(1)[0][0]
            counter[most_common_card] += n_jokers

        counts = sorted(counter.values(), reverse=True)
        match counts:
            case [5]:
                return 6
            case [4, 1]:
                return 5
            case [3, 2]:
                return 4
            case [3, 1, 1]:
                return 3
            case [2, 2, 1]:
                return 2
            case [2, 1, 1, 1]:
                return 1
            case _:
                return 0


def load_data() -> list[Hand]:
    """Load the poker hands."""
    with DATA_PATH.open("r", encoding="utf-8") as file:
        lines = map(str.rstrip, file)
        hands = []
        for line in lines:
            cards, bet_str = line.split(" ", 1)
            hands.append(Hand(cards, int(bet_str)))  # type: ignore
        return hands


def count_winnings(hands: list[Hand]) -> Bet:
    """Count the total winnings from the hands."""
    hands = sorted(
        hands, key=lambda hand: (hand.get_rank(), hand.get_card_values(), hand.bet)
    )
    return sum(rank * hand.bet for rank, hand in enumerate(hands, 1))


def count_winnings_with_jokers(hands: list[Hand]) -> Bet:
    """Count the total winnings from the hands using jokers."""
    hands = sorted(
        hands,
        key=lambda hand: (hand.get_rank(True), hand.get_card_values(True), hand.bet),
    )
    return sum(rank * hand.bet for rank, hand in enumerate(hands, 1))


def main():
    """Run the advent of code solution."""
    hands = load_data()
    print("Total winnings:", count_winnings(hands))
    print("Total winnings with jokers:", count_winnings_with_jokers(hands))


if __name__ == "__main__":
    main()
