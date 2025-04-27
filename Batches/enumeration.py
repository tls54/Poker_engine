from poker_engine.back_end import Deck, Card
from poker_engine.utils import hand_to_cpp
from poker_engine.hand_eval import evaluate_hand

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


NUM_PLAYERS = 6

deck = Deck()

# Deal hole cards
player_hands = [deck.deal(2) for _ in range(NUM_PLAYERS)]

rest_of_cards = deck.deal(52 - (2*NUM_PLAYERS))

print(len(rest_of_cards))



