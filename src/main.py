#!/usr/bin/env python
'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/main.py
Purpose:    play the game here

Before running make sure locale lang is UTF-8
```
export LANG=en_US.UTF-8
export LANGUAGE=en_US.en
export LC_ALL=en_US.UTF-8
```

'''

from game import ERS
from printer import *

splash = """
  _                                     _                __                   
 |_   _       ._   _|_  o   _.  ._     |_)   _.  _|_    (_    _  ._   _       
 |_  (_|  \/  |_)   |_  |  (_|  | |    | \  (_|   |_    __)  (_  |   (/_  \/\/
      _|  /   |                                                               
-------------------------------------------------------------------------------
"""
rules = """
Rules found here: (https://www.bicyclecards.com/how-to-play/egyptian-rat-screw/)

Double\t\tWhen two cards of equivalent value are laid down consecutively. Ex: 5, 5
Sandwich\tWhen two cards of equivalent value are laid down consecutively, but with one card of different value between them. Ex: 5, 7, 5
Top Bottom\tWhen the same card as the first card of the set is laid down.
Tens\t\tWhen two cards played consecutively (or with a letter card in between) add up to 10. For this rule, an ace counts as one. Ex: 3, 7 or A, K, 9
Jokers\t\tWhen jokers are used in the game, which should be determined before gameplay begins. Anytime someone lays down a joker, the pile can be slapped.
Four in a row\tWhen four cards with values in consistent ascending or descending order is placed. Ex: 5, 6, 7, 8 or Q, K, A, 2
Marriage\tWhen a queen is placed over or under a king. Ex: Q, K or K,Q
"""


def main():

  numOfPlayers = 2

  game = ERS(numOfPlayers)

  print(splash + rules)
  game.start_game()


if __name__ == '__main__':
  main()
