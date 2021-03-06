#!/usr/bin/env python
'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/cards.py
Purpose:    define Card, Deck, Hand classes

'''

import ctypes

from functools import total_ordering
from random import shuffle
from printer import *


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
    value_ERS(self)
        Get ERS value of Card
    is_face(self)
        Checks if Card is face card (J, Q, K, or A)
    """

  suits = ['♦', '♣', '♥', '♠']
  ranks = [
      None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
  ]

  def __init__(self, suit=0, rank=0):
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
    return "{}({} {})".format(self.__class__.__name__, self.suit, self.rank)

  def __str__(self):
    """Stringify"""
    return '|{:^2}{}|'.format(self.ranks[self.rank], self.suits[self.suit])
    # return "|%s%s|" % (self.ranks[self.rank], self.suits[self.suit])

  def value_ERS(self):
    """Get ERS value of Card"""
    if self.rank == 11:
      return 1
    elif self.rank == 12:
      return 2
    elif self.rank == 13:
      return 3
    elif self.rank == 1:
      return 4
    else:
      return 0

  def is_face(self):
    """Checks if Card is face card (J, Q, K, or A)"""
    if 11 <= self.rank <= 13 or self.rank == 1:
      return True
    else:
      return False


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
    is_empty(self)
        Checks if CardStack is empty
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
    return "{} [{}]".format(self.__class__.__name__, ", ".join(
        repr(c) for c in self.stack))

  def __str__(self):
    """Stringify"""

    if self.size > 13:
      # If longer than 13, print shortened version with elipses
      return "  ... {}".format(" ".join(str(c) for c in self.stack[-9:]))
    else:
      # Otherwise print 10 cards
      return "{}".format(" ".join(str(c) for c in self.stack))

  def is_empty(self):
    """Checks if CardStack is empty
        
        Returns
        -------
        bool
            Indicates True if CardStack is empty, False if not
        """

    return self.size == 0

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

    if not self.is_empty():
      # Must be nonmutable to propagate through namespace:
      # https://stackoverflow.com/questions/9436757/how-does-multiprocessing-manager-work-in-python

      temp = self.stack
      removed = temp.pop(i)

      self.stack = temp
      self.size -= 1

      return removed
    else:
      raise IndexError("Cannot perform operation on empty %s.",
                       self.__class__.__name__)

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

    self.stack += [card]
    self.size += 1

  def prepend(self, card):
    """Add Card to front of stack
        
        Parameters
        ----------
        card : Card
            Card to add to front of stack
        
        """

    self.stack = [card] + self.stack
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

  def to_hand(self, player, num, toTop=False):
    """Move top `num` Cards from deck to top/bottom of player's Hand
        
        Parameters
        ----------
        player : Player
            Player to give cards to
        num : int
            Number of cards to move to Hand
        toTop : bool, optional
            Indicates if card from hand should be added to top or 
            bottom of Deck (the default is False, which is bottom)

        """

    # print("Adresses inside deck: " + str(id(self)))
    # print("Adresses inside player: " + str(id(player)))
    # print("Deck object in class:")
    # print(ctypes.cast(id(self), ctypes.py_object).value)

    if not self.is_empty():
      if toTop:
        for i in range(num):
          # print(self)
          player.hand.append(self.pop())
      else:
        for i in range(num):
          # print(self.size)
          player.hand.prepend(self.pop())
    else:
      raise IndexError(
          "Cannot perform operation on empty %s." % self.__class__.__name__)


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

    if not self.is_empty():
      if toTop:
        for i in range(num):
          deck.append(self.pop())
      else:
        for i in range(num):
          deck.prepend(self.pop())
    else:
      raise IndexError(
          "Cannot perform operation on empty %s." % self.__class__.__name__)
