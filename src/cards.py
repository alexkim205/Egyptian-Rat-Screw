'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/cards.py
Purpose:    define deck, hand, and card classes

'''

from functools import total_ordering

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
    size
        Number of cards in deck
    
    Methods
    -------
    __init__(self, size)
        Initialize a stack of cards of certain size
    pop(self, i=-1)
        Pop off ith Card from top of stack
    peek(self)
        Look at Card at top of stack
    append(self, Card)
        Add Card to top of stack
    prepend(self, Card)
        Add Card to front of stack
    remove(self, Card)
        Remove Card from stack
    
    """

    def __init__(self, size):
        """Initialize a stack of cards of certain size
        
        Parameters
        ----------
        size : int
            Size of stack of cards
        
        """
        self.stack = []
        self.size = size

    def pop(self, i=-1):
                
        """Pop off ith Card from top of stack"""

    def peek(self):
        """Look at Card at top of stack"""

    def append(Card):
        """Add Card to top of stack"""
    
    def prepend(Card):
        """Add Card to front of stack"""
    
    def remove(Card):
        """Remove Card from stack"""
    

class Deck(CardStack):
    """A whole deck of cards
    
    Implement stack data structure.

    Attributes
    ----------
    size
        number of cards in deck
    
    Methods
    -------
    __init__(self, size)
        Initialize a stack of 52 cards

    remove(Card)
        Remove Card from deck
    shuffle()
        Shuffle the deck
    to_hand()
        Sort the deck in ascending order
    """

    def __init__(self):
        super().__init__(self, 52)

    
class Hand():
    """The hand that the player is holding
    """
