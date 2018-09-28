#!/usr/bin/env python3
"""
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/game.py
Purpose:    define game class

"""

import ctypes

# from multiprocessing import Process, Condition, Lock, Queue
from threading import Lock, Thread, Event
import queue
import time

from player import User, Computer
from cards import Deck
from printer import *

from cpu import GameManager


class ERS:

  def __init__(self, numOfPlayers):

    self.numOfPlayers = numOfPlayers
    self.numOfCardsPerPlayer = 52 // numOfPlayers
    # self.playerDict =
    self.players = []
    self.turns = [queue.Queue(maxsize=1) for _ in range(numOfPlayers)]

    # Initialize lock to put around Deck object
    self.lock = Lock()  # lock around accessing deck data

    # Initialize event locks for each player thread
    # self.events = [Event() for _ in range(nu∏mOfPlayers)]
    self.threads = []

  def __str__(self):

    playersScores = [
        "Player {} has {} cards".format(i, player.hand.size)
        for i, player in enumerate(self.players)
    ]

    return "; ".join(playersScores)

  def ticker(self):
    counter = 0
    # activate queue
    self.turns[0].put(1)
    print_turns(self)

  def start_game(self):

    print_info("Game started!")

    # Initialize Deck
    deck = Deck()
    deck.shuffle()
    print_deck(deck)

    # Initialize all players
    print_info("Dealing {} cards each to {} players".format(
        self.numOfCardsPerPlayer, self.numOfPlayers))

    # Initialize player 0 - fork subprocess
    user_id = 0
    playerProcess = Thread(target=self.player_process, args=(user_id, deck))

    self.threads.append(playerProcess)

    # Initialize CPU's - fork subprocesses for CPU's
    for cpu_id in range(1, self.numOfPlayers):

      # CPU Processes
      cpuProcess = Thread(target=self.cpu_process, args=(cpu_id, deck))

      self.threads.append(cpuProcess)

    # for event in self.events:
    #     event.set() # set each event
    # set player event
    for thread in self.threads:
      thread.start()
    # for thread in self.threads:
    #     thread.join()

    # Start game ticker to set turns
    # time.sleep(1)
    print("Game in 3")
    # time.sleep(1)
    print("Game in 2")
    # time.sleep(1)
    print("Game in 1")

    print("Starting ticker")
    self.ticker()

    print_score(self)

  def controller(self, deck):
    pass

  def player_process(self, id, deck):

    me = User(id)

    myQueue = self.turns[id]
    nextQueue = self.turns[(id + 1) % self.numOfPlayers]

    self.players.append(me)
    deck.to_hand(me, self.numOfCardsPerPlayer)
    me.turnsLeft = 1

    while True:

      # If player's turn
      if not myQueue.empty():

        # Implement game logic here

        if me.turnsLeft > 0:
          # if there are still turns left, don't change turns
          print("it's your turn")
          print_turnsLeft(self)

          response = input("> ")

          if response == "f":
            # spit
            me.spit(deck)
            print_deck(deck)
            print_player("Player {} has {} cards".format(id, me.hand.size), id)
            me.turnsLeft -= 1
            nextPlayer = self.players[(id + 1) % self.numOfPlayers]

            value_of_last_card = deck.peek().value_ERS()

            if value_of_last_card > 0:
              # If the card just placed down is special, go to next player
              me.turnsLeft = 0
              nextPlayer.turnsLeft = value_of_last_card
              nextPlayer.hasToBeat = True
            elif me.turnsLeft == 0:
              # If last card was placed down, check if go to next player
              if value_of_last_card == 0 and me.hasToBeat:
                # If value of last card is 0 and player had to beat other player's face card but lost, then other player takes deck
                deck.to_hand(nextPlayer, deck.size)
              elif value_of_last_card == 0 and not me.hasToBeat:
                # If value of last card is 0 and player didn't have to beat other player's face card, then play continues
                pass
              me.hasToBeat = False
              nextPlayer.turnsLeft = 1
              nextPlayer.hasToBeat = False

          elif response == "j":
            # slap
            me.slap(deck)

        elif me.turnsLeft == 0:
          # if there are no turns left, change turns

          # pop everything off my queue
          for q in self.turns:
            with q.mutex:
              q.queue.clear()
          # push 1 to next turn
          nextQueue.put(1)

  def cpu_process(self, id, deck):

    cpu = Computer(id)
    myQueue = self.turns[id]
    nextQueue = self.turns[(id + 1) % self.numOfPlayers]

    self.players.append(cpu)
    deck.to_hand(cpu, self.numOfCardsPerPlayer)

    print_player(cpu, cpu.id)

    while True:

      if not myQueue.empty():
        # If player's turn

        # Implement game logic here
        cpu.slap(deck)

        # Spit accordingly

        if cpu.turnsLeft > 0:
          # if there are still turns left, don't change turns
          print("it's cpu's turn")
          print_turnsLeft(self)

          # spit
          cpu.spit(deck)
          print_deck(deck)
          print_player("Player {} has {} cards".format(id, cpu.hand.size), id)
          cpu.turnsLeft -= 1
          nextPlayer = self.players[(id + 1) % self.numOfPlayers]
          
          value_of_last_card = deck.peek().value_ERS()

          if value_of_last_card > 0:
            # If the card just placed down is special, go to next player
            cpu.turnsLeft = 0
            nextPlayer.turnsLeft = value_of_last_card
            nextPlayer.hasToBeat = True
          elif cpu.turnsLeft == 0:
            # If last card was placed down, check if go to next player
            if value_of_last_card == 0 and cpu.hasToBeat:
              # If value of last card is 0 and player had to beat other player's face card but lost, then other player takes deck
              deck.to_hand(nextPlayer, deck.size)
            elif value_of_last_card == 0 and not cpu.hasToBeat:
              # If value of last card is 0 and player didn't have to beat other player's face card, then play continues
              pass
            cpu.hasToBeat = False
            nextPlayer.turnsLeft = 1
            nextPlayer.hasToBeat = False

        elif cpu.turnsLeft == 0:
          # if there are no turns left, change turns

          # pop everything off my queue
          for q in self.turns:
            with q.mutex:
              q.queue.clear()
          # push 1 to next turn
          nextQueue.put(1)

      else:
        # Still check if cpu can slap

        cpu.slap(deck)

  def winner_exists(self):
    """Checks if a winner exists

        Returns
        -------
        boolean
          A boolean that tells you if there is a winner
        """

    playersWithCards = [
        i for i, player in enumerate(self.players) if not player.hand.size == 0
    ]

    if len(playersWithCards) == 1:
      return True
    else:
      return False
