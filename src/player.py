#!/usr/bin/env python

'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/player.py
Purpose:    define player class

'''

from cards import Hand

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

    def __repr__(self):
        """Representational string representation"""
        return "%s(%s)" % (self.__class__.__name__, repr(self.hand))
    
    def __str__(self):
        """Stringify"""

        return "%s %s has %s cards" % (self.__class__.__name__, self.id, self.hand.size)

    def spit(self, deck):
        """The player moves top card from hand to top of main deck
        
        Parameters
        ----------
        deck : Deck
            The main deck to move card to
        
        """

        self.hand.to_deck(deck, 1, toTop=True)
    
    def burn(self, deck):
        """The player "burns" top card from hand to bottom of main deck
        
        Parameters
        ----------
        deck : Deck
            The main deck to move card to
        
        """

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

        if(self._check_slap(deck)):
            # Good slap -> move all deck cards to hand
            deck.to_hand(self.hand, deck.size)
            
        else:
            # Bad slap -> burn one card to front of deck
            self.burn(deck)

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

        if (
            # Double
            deck.stack[-1] == deck.stack[-2] or
            # Sandwich
            deck.stack[-1] == deck.stack[-3] or
            # Top Bottom
            deck.stack[-1] == deck.stack[0] or
            # Tens
            (deck.stack[-1].rank + deck.stack[-2].rank == 10) or 
            (11 <= deck.stack[-2].rank <= 13 and sum([e.rank for e in deck.stack[-3:]]) == 10) or
            # Jokers
            deck.stack[-1].rank == 11 or
            # Four in a row
            all(diff == 1 for diff in [y - x for x, y in zip(deck.stack[-4:-1], deck.stack[-3:])]) # get differences
            # Marriage 
            (deck.stack[-1] == 12 and deck.stack[-2] == 13) or
            (deck.stack[-1] == 13 and deck.stack[-2] == 12)
        ): 
            slapIsGood = True

        return slapIsGood


class Computer(Player):

    # 1 (beginner CPU) - 5 (hard CPU)
    seeds = range(5)

    def __init__(self, id=''):
        """Initialize player object"""
        
        self.hand = Hand()
        self.seed = 0
    
    