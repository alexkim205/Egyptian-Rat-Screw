'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/cards.py
Purpose:    define deck, hand, and card classes

'''

from functools import total_ordering
from random import shuffle

@total_ordering
class Card(): 
    """A playing card.

    Attributes
    ----------
    suit : int
        An integer from 0-3 indicating Clubs, Diamonds, Hearts, or Spades
    rank : int
        An integer from 0-13, 0 indicates none

    Methods
    -------
    __init__(self, suit, rank)
        Initialize Card with suit and rank; defaults to Diamonds 'None'
    __eq__(self, other)
        Checks = of self to other Card
    __ne__(self, other)
        Checks != of self to other Card
    __lt__(self, other)
        Checks < equality of self to other Card
    __repr__(self)
        String representation
    """

    suits = ["Diamonds", "Clubs", "Hearts", "Spades"]
    ranks = [None, "A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    def __init__(self, suit = 0, rank = 0):
        """Initialize Card with suit and rank; defaults to Diamonds 'None'"""
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):
        """Checks = of self to other Card"""
        return ((self.suit, self.rank) == (other.suit, other.rank))

    def __ne__(self, other):
        """Checks != of self to other Card"""
        return not (self == other)
        
    def __lt__(self, other):
        """Checks < equality of self to other Card"""
        return ((self.suit, self.rank) < (other.suit, other.rank))

    def __repr__(self):
        """String representation"""
        return "Card (%s %s)" % (self.suit, self.rank)

class CardStack():
    """A stack of cards. 
    
    Implement stack data structure.

    Attributes
    ----------
    stack : list
        List of cards in deck
    size : int
        Number of cards in deck, starts at 0
    
    Methods
    -------
    __init__(self)
        Initialize an empty stack of cards
    pop(self, i=-1)
        Pop off ith Card from top of stack
    peek(self)
        Look at Card at top of stack
    append(self, card)
        Add Card to top of stack
    prepend(self, card)
        Add Card to front of stack
    
    """

    def __init__(self):
        """Initialize an empty stack of cards"""

        self.stack = []
        self.size = 0

    def pop(self, i=-1):
        """Pop off ith Card from top of stack
        
        Parameters
        ----------
        i : int, optional
            Index of element to pop (the default is -1, which is it the last element)
        
        Returns
        -------
        Card
            Card that is popped off stack
        """

        return self.stack.pop(i)        

    def peek(self):
        """Look at Card at top of stack
        
        Returns
        -------
        Card
            Card at top of stack
        """

        return self.stack[-1]

    def append(self, card):
        """Add Card to top of stack
        
        Parameters
        ----------
        card : Card
            Card to add to top of stack
        
        """

        self.stack.append(card)
    
    def prepend(self, card):
        """Add Card to front of stack
        
        Parameters
        ----------
        card : Card
            Card to add to front of stack
        
        """

        self.stack.insert(0, card)
    

class Deck(CardStack):
    """A whole deck of cards

    Attributes
    ----------
    stack : list
        List of cards in deck
    size: int
        Number of cards in deck
    
    Methods
    -------
    __init__(self, size)
        Initialize a stack of 52 cards
    shuffle(self)
        Shuffle the deck
    to_hand(self, hand, num)
        Move top [num] Cards from deck to Hand

    """

    def __init__(self):
        """Initialize a stack of the 52 cards of a standard deck"""

        super().__init__(self)
        self.size = 52

        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.stack.append(card)
    
    def shuffle(self):
        """Shuffle deck"""
        shuffle(self.stack)
    
    def deck_to_hand(self, hand, num):
        """Move top [num] Cards from deck to Hand
        
        Parameters
        ----------
        hand : Hand
            Hand to add cards to
        num : int
            Number of cards to move to Hand

        """

        self.stack.pop()

    
class Hand(CardStack):
    """A player's hand

    Attributes
    ----------
    stack : list
        List of cards in hand
    size: int
        Number of cards in hand
    
    Methods
    -------
    __init__(self, size)
        Initialize an empty hand

    """

    def __init__(self):
        """Initialize an empty hand"""

        super().__init__(self)
    