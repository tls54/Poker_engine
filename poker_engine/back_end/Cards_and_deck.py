import random

RANKS = "AKQJT98765432"
SUITS = "cdhs"  # clubs, diamonds, hearts, spades


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return str(self)

class Deck:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.cards = [Card(r, s) for r in RANKS for s in SUITS]
        random.shuffle(self.cards) # Shuffle is built into the class
    
    def deal(self, num=1):
        return [self.cards.pop() for _ in range(num)]