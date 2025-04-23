import random
import statistics
from time import perf_counter
import matplotlib.pyplot as plt
from Python_ranking import evaluate_hand as python_evaluate_hand, card_str_to_int
from poker_engine.hand_eval import evaluate_hand  # type: ignore

RANKS = '23456789TJQKA'
SUITS = 'cdhs'

def generate_random_hand(num_players=6):
    deck = [r + s for r in RANKS for s in SUITS]
    random.shuffle(deck)
    hands = [deck[i*2:(i+1)*2] for i in range(num_players)]
    board = deck[num_players*2:num_players*2 + 5]
    return hands, board

def collect_timings(evaluate_fn, warmup_rounds=1_000, num_rounds=10_000, num_players=6):
    # Warmup
    for _ in range(warmup_rounds):
        hands, board = generate_random_hand(num_players)
        for hand in hands:
            all_cards = [card_str_to_int(c) for c in hand + board]
            _ = evaluate_fn(all_cards)

    # Timing
    timings = []
    for _ in range(num_rounds):
        hands, board = generate_random_hand(num_players)
        for hand in hands:
            all_cards = [card_str_to_int(c) for c in hand + board]
            start = perf_counter()
            _ = evaluate_fn(all_cards)
            timings.append((perf_counter() - start) * 1e6)  # µs

    return timings

def summarize(label, timings):
    print(f"\nSummary for {label}:")
    print(f"  Samples: {len(timings)}")
    print(f"  Mean:    {statistics.mean(timings):.4f} µs")
    print(f"  Median:  {statistics.median(timings):.4f} µs")
    print(f"  Stdev:   {statistics.stdev(timings):.4f} µs")
    print(f"  Min:     {min(timings):.4f} µs")
    print(f"  Max:     {max(timings):.4f} µs")

def plot_distributions(results, clamp_percentile=99.5):
    plt.figure(figsize=(10, 5))

    # Determine clamping range to exclude outliers
    all_times = [t for _, times in results for t in times]
    max_x = statistics.quantiles(all_times, n=1000)[int(clamp_percentile * 10)]

    for label, times in results:
        clamped_times = [t for t in times if t <= max_x]
        plt.hist(clamped_times, bins=100, alpha=0.6, label=label, edgecolor='black')

    plt.title("Hand Evaluation Time Distribution")
    plt.xlabel("Time per hand (µs)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    python_times = collect_timings(python_evaluate_hand)
    cpp_times = collect_timings(evaluate_hand)

    summarize("Python Hand Evaluator", python_times)
    summarize("C++ Hand Evaluator", cpp_times)

    plot_distributions([
        ("Python Evaluator", python_times),
        ("C++ Evaluator", cpp_times)
    ])