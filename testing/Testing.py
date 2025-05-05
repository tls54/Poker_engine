from poker_engine.hand_eval import evaluate_hand # type: ignore
from poker_engine.utils import hand_to_cpp
from poker_engine.back_end.Cards_and_deck import Card, Deck
from time import perf_counter

NUM_PLAYERS = 6

deck = Deck()

# Deal hole cards
player_hands = [deck.deal(2) for _ in range(NUM_PLAYERS)]

# Deal board
board = deck.deal(5)

# Concat player hole cards and board 
player_full_hands = [player_hand + board for player_hand in player_hands]

# Convert to cpp representations
converted_hands = [hand_to_cpp(hand) for hand in player_full_hands]

start = perf_counter()
# Run hands through cpp hand ranking and evaluation
outputs = [evaluate_hand(hand) for hand in converted_hands]
end = perf_counter()
# Extract scores and hand types
scores = [output[0] for output in outputs]
hand_types = [output[1] for output in outputs]

# Locate winning hand in hands
winner_index = scores.index(max(scores))

print(f"Player: {player_hands}")
print(f'Board: {board}')

for i in range(NUM_PLAYERS):
    print(f'hand: {player_hands[i]}, type: {hand_types[i]}, score: {scores[i]}')

print('Winner:')
print(f'Winning hand: {player_hands[winner_index]}')
print(f"Hand type: {hand_types[winner_index]}")
print(f"Score: {scores[winner_index]}")
print()
print(f'C++ eval time for {NUM_PLAYERS} players: {end - start}s')