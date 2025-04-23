import numpy as np
from .Cards_and_deck import RANKS


class Player:
    def __init__(self, name, range_matrix):
        self.name = name
        self.range_matrix = range_matrix
        self.hole_cards = []
        self.all_in_hand = False
    
    def receive_cards(self, cards):
        # Use with deck.deal in cards parameter
        self.hole_cards = cards
    
    def decide_action(self):
        coords = self._hand_to_coords()
        if coords:
            row, col = coords
            self.all_in_hand = bool(self.range_matrix[row, col])
        else:
            self.all_in_hand = False  # default to fold on error

    def hand_to_type(self):
        try:
            card1, card2 = self.hole_cards
            r1 = RANKS.index(card1.rank)
            r2 = RANKS.index(card2.rank)
            # Check for pocket pair
            if r1 == r2:
                return (f'{card1.rank}{card2.rank}')
            
            elif card1.suit == card2.suit:
                # Larger rank number means lower ranked card (0,0) is aces
                if r2 > r1:
                    return (f'{card1.rank}{card2.rank}s')
                if r1 > r2:
                    return (f'{card2.rank}{card1.rank}s')
            
            else:
                if r2 > r1:
                    return (f'{card1.rank}{card2.rank}o')
                if r1 > r2:
                    return (f'{card2.rank}{card1.rank}o')
        except:
            return None


    def _hand_to_coords(self):
        try:
            card1, card2 = self.hole_cards
            r1 = RANKS.index(card1.rank)
            r2 = RANKS.index(card2.rank)
            # Check for pocket pair
            if r1 == r2:
                return (r1, r1)
            
            # Check for suited cards
            elif card1.suit == card2.suit:
                # Return higher ranked card first
                return (min(r1, r2), max(r1, r2))  # suited: upper triangle
            
            # Off-suited cards
            else:
                return (max(r1, r2), min(r1, r2))  # off-suited: lower triangle
        except:
            return None