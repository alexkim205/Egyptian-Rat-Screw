#!/usr/bin/env python
'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/player.py
Purpose:    define player class

'''

from cards import Hand
from printer import *

import random
import time


class Player:
  """
    A Player class

    Attributes
    ----------
    num_cards : int
        The number of cards the player has
    id : str
        A player's id

    Methods
    -------
    __init__(self, id='')
        Initialize player object
    __repr__(self)
        Representational string
    __str__(self)
        Stringify
    spit(self, deck)
        The player moves top card from hand to top of main deck
    burn(self, deck)
        The player "burns" top card from hand to bottom of main deck
    slap(self, deck)
        The player slaps the main deck

    """

  def __init__(self, id=''):
    """Initialize player object"""

    self.hand = Hand()
    self.id = id
    self.turnsLeft = 0
    self.hasToBeat = False
    # self.prevPlayer <- implement like linked list?
    # self.nextPlayer <- implement like linked list?

  def __repr__(self):
    """Representational string representation"""
    return "%s(%s)" % (self.__class__.__name__, repr(self.hand))

  def __str__(self):
    """Stringify"""

    return "%s" % (str(self.hand))
    # return "%s %s has %s cards" % (self.__class__.__name__, self.id, self.hand.size)

  def spit(self, deck):
    """The player moves top card from hand to top of main deck

        Parameters
        ----------
        deck : Deck
            The main deck to move card to

        """

    temp = self.hand.peek()
    self.hand.to_deck(deck, 1, toTop=True)
    print_player("+ %s" % (temp), self, replace=True)

  def burn(self, deck):
    """The player "burns" top card from hand to bottom of main deck

        Parameters
        ----------
        deck : Deck
            The main deck to move card to

        """
    # print_player("- %s" % (self.hand.peek()), self)
    self.hand.to_deck(deck, 1, toTop=False)

  def slap(self, deck):
    """
        The player slaps the main deck. If the slap is good, 
            the entire deck is transferred to the players hand.
            If not, the player must burn one card.

        Parameters
        ----------
        deck : Deck
            The main deck that the player slapped

        """

    print_player("slapped the deck", self)

    slapRule = self._check_slap(deck)
    if (slapRule is not False):
      # Good slap -> move all deck cards to hand
      whoWon = "You" if self.id == 0 else "Player %d" % (self.id)
      print_player(
          "+ %d cards. %s won the deck with the %s!" % (deck.size, whoWon,
                                                             slapRule), self)
      deck.to_hand(self, deck.size, toTop=False)
      return True

    else:
      # Bad slap -> burn one card to front of deck
      temp = self.hand.peek()
      self.burn(deck)
      print_player("- %s Bad slap!" % (temp), self)
      return False

  @staticmethod
  def _check_slap(deck):
    """Check if deck is slappable 

        Rules found here: (https://www.bicyclecards.com/how-to-play/egyptian-rat-screw/)
        * Double – When two cards of equivalent value are laid down consecutively. Ex: 5, 5
        * Sandwich – When two cards of equivalent value are laid down consecutively, but with one card of different value between them. Ex: 5, 7, 5
        * Top Bottom – When the same card as the first card of the set is laid down.
        * Tens – When two cards played consecutively (or with a letter card in between) add up to 10. For this rule, an ace counts as one. Ex: 3, 7 or A, K, 9
        * Jokers – When jokers are used in the game, which should be determined before gameplay begins. Anytime someone lays down a joker, the pile can be slapped.
        * Four in a row – When four cards with values in consistent ascending or descending order is placed. Ex: 5, 6, 7, 8 or Q, K, A, 2
        * Marriage – When a queen is placed over or under a king. Ex: Q, K or K,Q

        Parameters
        ----------
        deck : Deck
            The Deck that you want to check

        Returns
        -------
        boolean
            True if deck was slappable, False if not
        """

    slapIsGood = False
    slapRule = None
    slapLogFormat = "{} Rule"

    def deck1(_deck):
      # """If deck is 1 card

      #       * Jokers
      #       """

      # if _deck.stack[-1].rank == 11:
      #   _slapRule = slapLogFormat.format("Jokers")
      #   return True
      # return False
      return []  # don't implement Joker card

    def deck2(_deck):
      """If deck is 2 cards

            * Double
            * Top Bottom
            * Tens - 2 cards
            * Marriage
            """

      if _deck.stack[-1].rank == _deck.stack[-2].rank:
        return [slapLogFormat.format("Double")]
      if _deck.stack[-1].rank == _deck.stack[0].rank:
        return [slapLogFormat.format("Top Bottom")]
      if _deck.stack[-1].rank + _deck.stack[-2].rank == 10:
        return [slapLogFormat.format("Tens - 2 cards")]
      if (_deck.stack[-1].rank == 12 and _deck.stack[-2].rank == 13) or \
              (_deck.stack[-1].rank == 13 and _deck.stack[-2].rank == 12):
        return [slapLogFormat.format("Marriage")]
      return []

    def deck3(_deck):
      """If deck is 3 cards

            * Sandwich
            * Tens - 3 cards
            """

      if _deck.stack[-1].rank == _deck.stack[-3].rank:
        return [slapLogFormat.format("Sandwich")]
      if 11 <= _deck.stack[-2].rank <= 13 and sum(
          [e.rank for e in _deck.stack[-3:]]) == 10:
        return [slapLogFormat.format("Tens - 3 cards")]
      return []

    def deck4(_deck):
      """If deck is 4 cards

            * Four in a row
            """

      if all(diff == 1 for diff in [
          y.rank - x.rank for x, y in zip(_deck.stack[-4:-1], _deck.stack[-3:])
      ]):
        return [slapLogFormat.format("Four in a row")]
      return []

    if deck.size == 1:
      slapRule = deck1(deck)

    elif deck.size == 2:
      slapRule = deck1(deck) + deck2(deck)

    elif deck.size == 3:
      slapRule = deck1(deck) + deck2(deck) + deck3(deck)

    elif deck.size >= 4:
      slapRule = deck1(deck) + deck2(deck) + deck3(deck) + deck4(deck)

    else:
      slapRule = []

    if len(slapRule) == 0:
      return False
    else:
      return slapRule[0]


class User(Player):

  def __init__(self, id='0'):
    super().__init__(id)


class Computer(Player):

  def __init__(self, id=''):
    """Initialize CPU object"""

    super().__init__(id)

    # self.id = "CPU" + str(id)
    self.hand = Hand()
    self.seed = random.seed()
    # 1 is no error, 0 is never slap
    self.errorSlapRate = 0.5  # random.uniform(0, 1) # TODO: not uniform

  def spit(self, deck):
    """Inherit spit with a random delay
    
      Parameters
      ----------
      deck : Deck
          The main deck to move card to
    
    """
    spitTime = random.uniform(0, 1)
    time.sleep(spitTime)
    super().spit(deck)

  def slap(self, deck):
    """Inherit slap with a random delay and random error
    
      Parameters
      ----------
      deck : Deck
          The main deck to move card to
    
    """

    if random.random() < self.errorSlapRate:
      slapTime = random.uniform(
          0.5, 1)  # probably convert to property for different diffculty levels
      time.sleep(slapTime)
      super().slap(deck)  # lmao a super slap
