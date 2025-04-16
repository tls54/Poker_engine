import sys 
import os
# Add project root to PYTHONPATH dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from time import perf_counter
from Benchmarks.Python_ranking import evaluate_hand as python_evaluate_hand, card_str_to_int
from engine.python.Back_end.hand_eval import evaluate_hand  # type: ignore

RANKS = '23456789TJQKA'
SUITS = 'cdhs'

def generate_random_hand(num_players=6):
    """Generate a full board and unique hands for each player."""
    deck = [r + s for r in RANKS for s in SUITS]
    random.shuffle(deck)
    hands = [deck[i*2:(i+1)*2] for i in range(num_players)]
    board = deck[num_players*2:num_players*2 + 5]
    return hands, board

def benchmark_eval(evaluate_fn, label, num_rounds=10_000, num_players=6):
    total_time = 0
    for _ in range(num_rounds):
        hands, board = generate_random_hand(num_players)
        for hand in hands:
            all_cards = [card_str_to_int(c) for c in hand + board]
            start = perf_counter()
            _ = evaluate_fn(all_cards)
            total_time += (perf_counter() - start)
    avg_time = total_time / (num_rounds * num_players)
    print(f"Benchmarking {label}:")
    print(f"  Total time for {num_rounds} rounds x {num_players} players: {total_time:.6f}s")
    print(f"  Average time per hand: {avg_time * 1000:.4f} ms\n")

if __name__ == "__main__":
    benchmark_eval(python_evaluate_hand, "Python Hand Evaluator")
    benchmark_eval(evaluate_hand, "C++ Hand Evaluator")