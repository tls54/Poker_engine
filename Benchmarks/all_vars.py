from poker_engine.hand_eval import evaluate_hand
from poker_engine.back_end import Deck, Card
from poker_engine.utils import hand_to_cpp
from time import perf_counter
import statistics

def benchmark_batch(warmup, main, batch_size):
    sub_durations = []
    durations = []

    deck = Deck()
    hand = deck.deal(7)
    hand = hand_to_cpp(hand)

    # warmup runs
    for _ in range(warmup):
        evaluate_hand(hand)

    # run main loops if batches
    for _ in range(main): 
        # create random hand for each main loop   
        deck = Deck()
        hand = deck.deal(7)

        hand = hand_to_cpp(hand)
        start = perf_counter()

        for _ in range(batch_size):
            substart = perf_counter()
            evaluate_hand(hand)
            subend = perf_counter()
            sub_durations.append(subend - substart)

        end = perf_counter()
        durations.append(end - start)
    return durations, sub_durations

if __name__ == '__main__':
    # number of unique boards in 6max
    num_boards = 658008 
    
    durations, sub_durations = benchmark_batch(10000, 20, num_boards)

    print('Ran successfully!')
    print(f'Mean subprocess time: {statistics.mean(sub_durations)}')
    print(f'Mean process time: {statistics.mean(durations)}')
    
