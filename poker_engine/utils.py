# Utility files
RANKS = "AKQJT98765432"
REVERSE_RANKS = RANKS[::-1]  # "23456789TJQKA"
SUIT_MAP = {"s": 0, "h": 1, "d": 2, "c": 3}

## Converts cards and hands to the format used by C++ hand evaluation


def card_to_cpp(card):
    """
    Convert a Python Card object to an integer [0–51] for C++.
    Card.rank should be a string like 'A', 'K', ..., '2'
    Card.suit should be 's', 'h', 'd', 'c'
    """
    rank_index = REVERSE_RANKS.index(card.rank)
    suit_index = SUIT_MAP[card.suit]
    return suit_index * 13 + rank_index

def hand_to_cpp(cards):
    return [card_to_cpp(c) for c in cards]