# Egyptian Rat Screw
A UNIX command line card ERS/Slap game written in Python

## Prerequisites
* Python>=3.6
* [sneakysnek](https://github.com/SerpentAI/sneakysnek)

Make sure your lang locale is set to UTF-8 to properly display UTF-8 characters in your terminal. You can do this by running:

```bash
$ export LANG=en_US.UTF-8
$ export LANGUAGE=en_US.en
$ export LC_ALL=en_US.UTF-8
```

## How to play the game
```bash
$ python src/main.py

  _                                     _                __
 |_   _       ._   _|_  o   _.  ._     |_)   _.  _|_    (_    _  ._   _
 |_  (_|  \/  |_)   |_  |  (_|  | |    | \  (_|   |_    __)  (_  |   (/_  \/\/
      _|  /   |
-------------------------------------------------------------------------------

Rules found here: (https://www.bicyclecards.com/how-to-play/egyptian-rat-screw/)

Double		When two cards of equivalent value are laid down consecutively. Ex: 5, 5
Sandwich	When two cards of equivalent value are laid down consecutively, but with one card of different value between them. Ex: 5, 7, 5
Top Bottom	When the same card as the first card of the set is laid down.
Tens		When two cards played consecutively (or with a letter card in between) add up to 10. For this rule, an ace counts as one. Ex: 3, 7 or A, K, 9
Jokers		When jokers are used in the game, which should be determined before gameplay begins. Anytime someone lays down a joker, the pile can be slapped.
Four in a row	When four cards with values in consistent ascending or descending order is placed. Ex: 5, 6, 7, 8 or Q, K, A, 2
Marriage	When a queen is placed over or under a king. Ex: Q, K or K,Q
```


## TODO

* Make user input cleaner and more intuitive.
* Instead of using external library, [sneakysnek](https://github.com/SerpentAI/sneakysnek) to record keypresses, implement cross platform keyboard capture on my own.
