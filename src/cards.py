#!/usr/bin/env python

'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/cards.py
Purpose:    define Card, Deck, Hand classes

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
        Representational string
    __str__(self)
        Stringify
    """

    suits = ['♦', '♣', '♥', '♠']
    ranks = [None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

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
        """Representational string representation"""
        return "%s(%s %s)" % (self.__class__.__name__, self.suit, self.rank)
    
    def __str__(self):
        """Stringify"""
        return "%s of %s" % (self.suits[self.suit], self.ranks[self.rank])

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
    __repr__(self)
        Representational string
    __str__(self)
        Stringify
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
    
    def __repr__(self):
        """Representational string representation"""
        return "%s [%s]" % (self.__class__.__name__, ", ".join(repr(c) for c in self.stack))
    
    def __str__(self):
        """Stringify"""
        s = "{} of {} cards\n".format(self.__class__.__name__, self.size)
        for c in self.stack:
            s += "  " + str(c) + "\n"

        return s

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

        self.size -= 1
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
        self.size += 1
    
    def prepend(self, card):
        """Add Card to front of stack
        
        Parameters
        ----------
        card : Card
            Card to add to front of stack
        
        """

        self.stack.insert(0, card)
        self.size += 1
    

class Deck(CardStack):
    """A whole deck of cards, cards will be face up

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
    __str__(self)

    shuffle(self)
        Shuffle the deck
    to_hand(self, player, num)
        Move top [num] Cards from deck to player's Hand

    """

    def __init__(self):
        """Initialize a stack of the 52 cards of a standard deck"""

        super().__init__()
        self.size = 52

        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.stack.append(card)
    
    def shuffle(self):
        """Shuffle deck"""
        shuffle(self.stack)
    
    def to_hand(self, player, num):
        """Move top `num` Cards from deck to player's Hand
        
        Parameters
        ----------
        player : Player
            Player to give cards to
        num : int
            Number of cards to move to Hand

        """
        for i in range(num):
            player.hand.append(self.pop())

    
class Hand(CardStack):
    """A player's hand, cards will be face down

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
    to_deck(self, size)
        Move top `num` Cards from Hand to top/bottom of Deck

    """

    def __init__(self):
        """Initialize an empty hand"""

        super().__init__()
    
    def to_deck(self, deck, num, toTop=True):
        """Move top `num` Cards from Hand to top/bottom of Deck
        
        Parameters
        ----------
        deck : Deck
            Deck to add cards to
        num : int
            Number of cards to move to Deck
        toTop : bool, optional
            Indicates if card from hand should be added to top or 
            bottom of Deck (the default is True, which is top)
        
        """

        if toTop:
            for i in range(num):
                deck.append(self.pop())
        else:
            for i in range(num):
                deck.prepend(self.pop())
