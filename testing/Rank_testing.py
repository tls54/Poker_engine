import sys 
import os


from poker_engine.hand_eval import evaluate_hand 
from poker_engine.utils import hand_to_cpp
from poker_engine.back_end.Cards_and_deck import Card



# Define player hole cards to test rare hand combos
card1 = Card('2', 'h')
card2 = Card('2', 'd')

card3 = Card('K', 's')
card4 = Card('A', 's')




card5 = Card('Q', 's')
card6 = Card('J', 's')
card7 = Card('3', 's')
card8 = Card('3', 'd')
card9 = Card('3', 'h')


player1 = [card1, card2]
player2 = [card3, card4]

player_hands = [player1, player2]

NUM_PLAYERS = len(player_hands)

board = [card5, card6, card7, card8, card9]

# Concat player hole cards and board 
player_full_hands = [player_hand + board for player_hand in player_hands]

# Convert to cpp representations
converted_hands = [hand_to_cpp(hand) for hand in player_full_hands]

# Run hands through cpp hand ranking and evaluation
outputs = [evaluate_hand(hand) for hand in converted_hands]

# Extract scores and hand types
scores = [output[0] for output in outputs]
hand_types = [output[1] for output in outputs]

# Locate winning hand in hands
winner_index = scores.index(max(scores))

print(f"Player: {player_hands}")
print(f'Board: {board}')

for i in range(NUM_PLAYERS):
    print(f'hand: {player_hands[i]}, type: {hand_types[i]}, score: {scores[i]}')



print(f'Winning hand: {player_hands[winner_index]}')
print(f"Hand type: {hand_types[winner_index]}")
print(f"Score: {scores[winner_index]}")