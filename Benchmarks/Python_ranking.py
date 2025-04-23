from collections import Counter
from itertools import combinations
from time import perf_counter



# Constants
RANKS = '23456789TJQKA'
SUITS = 'cdhs'
RANK_TO_INT = {r: i for i, r in enumerate(RANKS)}
INT_TO_RANK = {i: r for r, i in RANK_TO_INT.items()}

HAND_RANKS = {
    'HIGH_CARD': 1,
    'ONE_PAIR': 2,
    'TWO_PAIR': 3,
    'THREE_OF_A_KIND': 4,
    'STRAIGHT': 5,
    'FLUSH': 6,
    'FULL_HOUSE': 7,
    'FOUR_OF_A_KIND': 8,
    'STRAIGHT_FLUSH': 9,
    'ROYAL_FLUSH': 10
}

def card_str_to_int(card):
    rank = RANK_TO_INT[card[0]]
    suit = SUITS.index(card[1])
    return rank + 13 * suit

def int_to_card(card_int):
    rank = card_int % 13
    suit = card_int // 13
    return RANKS[rank] + SUITS[suit]

def get_rank(card): return card % 13
def get_suit(card): return card // 13

def is_straight(ranks):
    ranks = sorted(set(ranks))
    if 12 in ranks:  # Ace high
        ranks.append(-1)
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return list(range(ranks[i+4], ranks[i]-1, -1))
    return []

def encode_score(rank, key_cards, kickers):
    score = (rank << 20)
    shift = 12
    all_cards = key_cards + kickers
    for r in all_cards[:5]: 
        score |= (r << shift)
        shift -= 4
    return score

def evaluate_hand(cards):
    assert len(cards) == 7
    ranks = [get_rank(c) for c in cards]
    suits = [get_suit(c) for c in cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    freq_rank = sorted(((count, r) for r, count in rank_counts.items()),
                    reverse=True, key=lambda x: (x[0], x[1]))

    # Flush or Straight Flush
    for suit, count in suit_counts.items():
        if count >= 5:
            suited = sorted([get_rank(c) for c in cards if get_suit(c) == suit], reverse=True)
            suited = list(dict.fromkeys(suited))  # Remove duplicates

            straight = is_straight(suited)
            if straight:
                if straight[0] == 12:
                    return encode_score(HAND_RANKS['ROYAL_FLUSH'], [12,11,10,9,8], []), "ROYAL_FLUSH"
                return encode_score(HAND_RANKS['STRAIGHT_FLUSH'], [straight[0]], []), "STRAIGHT_FLUSH"
            return encode_score(HAND_RANKS['FLUSH'], suited[:5], []), "FLUSH"

    # Four of a Kind
    if freq_rank[0][0] == 4:
        four = freq_rank[0][1]
        kickers = [r for r in ranks if r != four]
        kicker = max(kickers)
        return encode_score(HAND_RANKS['FOUR_OF_A_KIND'], [four], [kicker]), "FOUR_OF_A_KIND"

    # Full House
    if freq_rank[0][0] == 3:
        trips = freq_rank[0][1]
        pairs = [r for c, r in freq_rank[1:] if c >= 2]
        if pairs:
            return encode_score(HAND_RANKS['FULL_HOUSE'], [trips, max(pairs)], []), "FULL_HOUSE"

    # Three of a Kind
    if freq_rank[0][0] == 3:
        trips = freq_rank[0][1]
        kickers = [r for c, r in freq_rank[1:] for _ in range(c)]
        return encode_score(HAND_RANKS['THREE_OF_A_KIND'], [trips], sorted(kickers, reverse=True)[:2]), "THREE_OF_A_KIND"

    # Two Pair
    if freq_rank[0][0] == 2 and freq_rank[1][0] == 2:
        hp, lp = freq_rank[0][1], freq_rank[1][1]
        kickers = [r for c, r in freq_rank[2:] for _ in range(c)]
        return encode_score(HAND_RANKS['TWO_PAIR'], [hp, lp], sorted(kickers, reverse=True)[:1]), "TWO_PAIR"

    # One Pair
    if freq_rank[0][0] == 2:
        pair = freq_rank[0][1]
        kickers = [r for c, r in freq_rank[1:] for _ in range(c)]
        return encode_score(HAND_RANKS['ONE_PAIR'], [pair], sorted(kickers, reverse=True)[:3]), "ONE_PAIR"

    # Straight
    straight = is_straight(ranks)
    if straight:
        return encode_score(HAND_RANKS['STRAIGHT'], [straight[0]], []), "STRAIGHT"

    # High Card
    sorted_ranks = sorted(ranks, reverse=True)
    return encode_score(HAND_RANKS['HIGH_CARD'], [], sorted_ranks[:5]), "HIGH_CARD"

# Example usage
if __name__ == "__main__":
    from time import perf_counter

    board = ['2h', '2d', 'Qd', 'Td', '9d']
    players = [
        ['Kd', 'Jd'],
        ['2c', '2s'],
        ['Ah', 'Ks'],
        ['Tc', '9c'],
        ['Qh', 'Th'],
        ['3d', '3s']
    ]

    board_int = [card_str_to_int(c) for c in board]

    start = perf_counter()

    for i, hand in enumerate(players):
        all_cards = [card_str_to_int(c) for c in hand] + board_int
        score, label = evaluate_hand(all_cards)
        print(f"Player {i+1}: {hand}, Hand Type: {label}, Score: {score}")

    end = perf_counter()
    print(f"\nTotal evaluation time: {end - start:.6f} seconds")