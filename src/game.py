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

  # @staticmethod
  def player_process(self, id, deck):

    me = User(id)

    # == Entering the critical zone
    # self.lock.acquire()

    # playerEvent = self.events[id]

    # self.playerDict[id] = [me.id, True]
    self.players.append(me)
    deck.to_hand(me, self.numOfCardsPerPlayer)
    me.turnsLeft = 1

    def isStillTurn():
      """ Check if still player's turn.

            """

      if not deck.peek().value_ERS() == 0:
        # if the card that player put down is not face card,
        # then continue to ask for more cards
        return True
      else:
        # if card on top of stack is face card
        return False

    myQueue = self.turns[id]
    nextQueue = self.turns[(id + 1) % self.numOfPlayers]

    while True:

      # If not player's turn, continue
      if not myQueue.empty():
        print("it's your turn")
        print_deck(deck)

        # Implement game logic here

        # set turnsLeft if first turn
        if me.turnsLeft == 0:
          me.turnsLeft = deck.peek().value_ERS()

        response = input("> ")

        if response == "f":
          # slap
          me.spit(deck)
          me.turnsLeft -= 1

        elif response == "j":
          # spit
          me.slap(deck)

        # if there are still turns left, don't change turns
        if me.turnsLeft == 0:
          # pop everything off my queue
          for q in self.turns:
            with q.mutex:
              q.queue.clear()
          # push 1 to next turn
          nextQueue.put(1)

      else:

        pass

  def cpu_process(self, id, deck):

    myQueue = self.turns[id]
    nextQueue = self.turns[(id + 1) % self.numOfPlayers]

    cpu = Computer(id)

    # == Entering the critical zone
    # self.lock.acquire()

    # Append cpu: (int: index, bool: isTurn)
    # self.playerDict[id] = [cpu.id, False]
    self.players.append(cpu)
    deck.to_hand(cpu, self.numOfCardsPerPlayer)

    # self.lock.release()
    # == Exiting the critical zone

    print_player(cpu, cpu.id)

    # cpuEvent = self.events[id]

    # Player loop, keep playing cards until winner exists
    # old_len = len(deck)

    while True:

      try:

        whoseTurn = myQueue.get()

        # print("It is " + str(whoseTurn) + "'s turn")
        # print(cpu.id)

        if whoseTurn:

          # print("It is cpu's turn!")
          # Initialize keypress recorder

          print("doing cpu stuff")
          time.sleep(5)
          print("cpu stuff done, added 1 to next queue")

          # pop everything off my queue
          for q in self.turns:
            with q.mutex:
              q.queue.clear()
          # push 1 to next turn
          nextQueue.put(1)

          print_turns(self)

      except queue.Empty:
        print(".")

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
