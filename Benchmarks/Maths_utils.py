from time import perf_counter
import statistics
import matplotlib.pyplot as plt

def factorial(n: int) -> int:
    if n < 0:
        print('The number must be a positive integer!')
        return None
    elif type(n) != int:
        print('The number must be a positive integer!')
        return None
    
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n+1):
            result *= i
        return result


def Choose(n:int, k:int) -> int:
    if n < k:
        print('n must be greater than k!')
        return None
    if type(n) != int or type(k) != int:
        print('n and k must be integers')
        return None
    else:
        choices = factorial(n) / (factorial(k) * factorial((n-k)))
        return int(choices)


def benchmark_choose(n:int, k:int, warmup:int=10_000, main:int=1_000_000):
    # Warm-up phase
    for _ in range(warmup):
        Choose(n, k)

    # Benchmarking phase
    durations = []
    for _ in range(main):
        start = perf_counter()
        Choose(n, k)
        end = perf_counter()
        durations.append(end - start)

    min_time = min(durations)
    max_time = max(durations)
    mean_time = statistics.mean(durations)
    stddev_time = statistics.stdev(durations) if len(durations) > 1 else 0.0

    print(f"Benchmark results for Choose({n}, {k}):")
    print(f"  Runs: {main}")
    print(f"  Min Time:   {min_time:.6e} seconds")
    print(f"  Max Time:   {max_time:.6e} seconds")
    print(f"  Mean Time:  {mean_time:.6e} seconds")
    print(f"  Std Dev:    {stddev_time:.6e} seconds")
    
    return durations



if __name__ == '__main__':
    players = 6
    cards_left = 52 - (2 * players)  # full deck minus hole cards 
    print(f'Cards left: {cards_left}')
    print('Number of possible outcomes in a 6max game after flop:')

    # Number of unique boards 
    num_boards = Choose(cards_left, 5)
    
    print(f'Total possible 5 card boards in 6max: {num_boards:,}')
    print(f'Total calls to evalutate_hand: {players * num_boards:,}')
    
    #small_durations = benchmark_choose(cards_left, 2)
    #big_durations = benchmark_choose(52, 5)

