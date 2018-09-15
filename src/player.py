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
            deck.to_hand(self, deck.size, toTop=False)
            
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

        def deck1(_deck):
            """If deck is 1 card

            * Jokers
            """
            bool = _deck.stack[-1].rank == 11
            return bool

        def deck2(_deck): 
            """If deck is 2 cards

            * Double
            * Top Bottom
            * Tens - 2 cards
            * Marriage
            """
            bool = \
                _deck.stack[-1] == _deck.stack[-2] or \
                _deck.stack[-1] == _deck.stack[0] or \
                _deck.stack[-1].rank + _deck.stack[-2].rank == 10 or \
                (_deck.stack[-1].rank == 12 and _deck.stack[-2].rank == 13) or \
                (_deck.stack[-1].rank == 13 and _deck.stack[-2].rank == 12)

            return bool

        def deck3(_deck): 
            """If deck is 3 cards

            * Sandwich
            * Tens - 3 cards
            """
            bool = \
                _deck.stack[-1] == _deck.stack[-3] or \
                11 <= _deck.stack[-2].rank <= 13 and sum([e.rank for e in _deck.stack[-3:]]) == 10
            
            return bool
            
        def deck4(_deck): 
            """If deck is 4 cards
            
            * Four in a row
            """
            print([y.rank - x.rank for x, y in zip(_deck.stack[-4:-1], _deck.stack[-3:])])
            bool = all(diff == 1 for diff in [y.rank - x.rank for x, y in zip(_deck.stack[-4:-1], _deck.stack[-3:])])
            
            return bool

        if deck.size == 1:
            if deck1(deck):
                slapIsGood = True

        elif deck.size == 2:
            if deck1(deck) or deck2(deck):
                slapIsGood = True

        elif deck.size == 3:
            if deck1(deck) or deck2(deck) or deck3(deck):
                slapIsGood = True
        
        elif deck.size >= 4:
            if deck1(deck) or deck2(deck) or deck3(deck) or deck4(deck):
                slapIsGood = True

        else:
            slapIsGood = False

        return slapIsGood


class Computer(Player):

    # 1 (beginner CPU) - 5 (hard CPU)
    seeds = range(5)

    def __init__(self, id=''):
        """Initialize player object"""
        
        self.hand = Hand()
        self.seed = 0
    
    