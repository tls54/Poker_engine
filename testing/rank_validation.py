from poker_engine.hand_eval import evaluate_hand, batch_evaluate  # type: ignore
from poker_engine.utils import hand_to_cpp
from poker_engine.back_end.Cards_and_deck import Card

def card(rank: str, suit: str) -> Card:
    """Helper to create a card from string representations"""
    return Card(rank=rank, suit=suit)

def cpp(hand):
    return hand_to_cpp(hand)

def print_eval(name, hand):
    score, hand_type = evaluate_hand(cpp(hand))
    print(f"{name}: {hand}, Type: {hand_type}, Score: {score}")
    return hand_type

def test_individual_hands():
    """Test one example of each hand type."""
    hands = {
        "High Card": [
            card('2', 's'), card('5', 'd'), card('9', 'c'),
            card('J', 'h'), card('Q', 'd'), card('3', 'c'), card('7', 'h')
        ],
        "One Pair": [
            card('5', 's'), card('5', 'd'), card('9', 'c'),
            card('J', 'h'), card('Q', 'd'), card('3', 'c'), card('7', 'h')
        ],
        "Two Pair": [
            card('5', 's'), card('5', 'd'), card('J', 'c'),
            card('J', 'h'), card('Q', 'd'), card('3', 'c'), card('7', 'h')
        ],
        "Three of a Kind": [
            card('5', 's'), card('5', 'd'), card('5', 'c'),
            card('J', 'h'), card('Q', 'd'), card('3', 'c'), card('7', 'h')
        ],
        "Straight": [
            card('2', 's'), card('3', 'd'), card('4', 'h'),
            card('5', 'c'), card('6', 's'), card('9', 'd'), card('Q', 'h')
        ],
        "Flush": [
            card('2', 's'), card('5', 's'), card('7', 's'),
            card('9', 's'), card('K', 's'), card('3', 'c'), card('Q', 'h')
        ],
        "Full House": [
            card('4', 'd'), card('4', 'h'), card('4', 's'),
            card('9', 'c'), card('9', 'd'), card('2', 'h'), card('J', 'c')
        ],
        "Four of a Kind": [
            card('Q', 's'), card('Q', 'h'), card('Q', 'd'),
            card('Q', 'c'), card('5', 's'), card('2', 'd'), card('9', 'h')
        ],
        "Straight Flush": [
            card('5', 'h'), card('6', 'h'), card('7', 'h'),
            card('8', 'h'), card('9', 'h'), card('2', 'c'), card('Q', 'd')
        ],
        "Royal Flush": [
            card('T', 's'), card('J', 's'), card('Q', 's'),
            card('K', 's'), card('A', 's'), card('2', 'c'), card('3', 'd')
        ],
    }

    for name, hand in hands.items():
        result = print_eval(name, hand)
        assert result.replace('_', ' ') == name.upper().replace('_', ' '), f"Expected {name}, got {result}"

def test_batch_tie_and_win():
    """Test batch evaluator with tie and win cases."""
    hand1 = [card('2', 's'), card('3', 's')] + [card('4', 's'), card('5', 's'), card('6', 's'), card('9', 'h'), card('Q', 'd')]  # Straight flush
    hand2 = [card('9', 'd'), card('T', 'd')] + [card('J', 'd'), card('Q', 'd'), card('K', 'd'), card('3', 'h'), card('5', 's')]  # Flush
    hand3 = [card('A', 'c'), card('A', 'd')] + [card('A', 's'), card('K', 'h'), card('K', 'd'), card('2', 'h'), card('5', 's')]  # Full house
    hand4 = hand2[:]  # tie with hand2

    games = [[
        cpp(hand1), cpp(hand2), cpp(hand3), cpp(hand4),
        cpp(hand2), cpp(hand1)  # repeat for batch consistency
    ]]

    results = batch_evaluate(games)



    print(f'\nResult:')
    print(results)
    assert results[0] == [1, 3, 4], f"Expected players 1, 3, 4 to tie with straight flush, got {results[0]}"
    print(f"Batch test passed. Winners: {results[0]}")

if __name__ == "__main__":
    test_individual_hands()
    test_batch_tie_and_win()
    print("All tests passed.")