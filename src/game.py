#!/usr/bin/env python

"""
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/game.py
Purpose:    define game class

"""

import ctypes

# from multiprocessing import Process, Condition, Lock, Queue
from threading import Lock, Thread

from player import User, Computer
from cards import Deck
from printer import *

from cpu import GameManager

from sneakysnek.recorder import Recorder

# Initialize multiprocess Manager and Deck
lock = Lock()  # lock around accessing deck data


class ERS:

    def __init__(self, numOfPlayers):

        self.numOfPlayers = numOfPlayers
        self.numOfCardsPerPlayer = 52 // numOfPlayers
        self.players = []
        self.whoseTurn = []

        self.whoseTurn = [True] + ([False] * (numOfPlayers - 1))

    def start_game(self):

        print_info("Game started!")

        
        # manager = GameManager()
        # namespace = manager.Namespace()
        # print(namespace)
        # manager.start() 

        # print("Adresses of deck proxy: " + str(id(manager.Deck)))

        # Initialize Deck
        # deck = manager.Deck()
        deck = Deck()
        deck.shuffle()
        # print_deck(deck)

        # manager.start()

        # Initialize all players
        print_info(
            "Dealing {} cards each to {} players".format(
                self.numOfCardsPerPlayer, self.numOfPlayers
            )
        )
        # Initialize player 0 - fork subprocess

        print("DEBUG")

        # playerLock = Condition(lock)
        playerProcess = Thread(
            target=self.player_process,
            args=(self.players, self.whoseTurn, deck, self.numOfCardsPerPlayer, lock))

        playerProcess.start()

        print("PLAYER 0 subprocess started.")

        # Initialize CPU's - fork subprocesses for CPU's
        listOfCPU = []
        for cpu_id in range(1, self.numOfPlayers):
            # CPU Processes
            # cpuLock = Condition(lock)
            cpuProcess = Thread(target=self.cpu_process,
                                    args=(self.players, self.whoseTurn, deck, self.numOfCardsPerPlayer, lock))

            cpuProcess.start()
            listOfCPU.append(cpuProcess)

        print("All CPU subprocesses started.")

        print("Main program continues")

        for p in [playerProcess] + listOfCPU:
            p.join()

    def controller(self, deck):
        pass

    @staticmethod
    def player_process(playerList, turnList, deck, numOfCardsPerPlayer, _lock):
        import os
        print("Process ID:", os.getpid())

        me = User()
        playerList.append(me)

        # == Entering the critical zone
        _lock.acquire()

        print("before:", str(deck.size))
        remove = deck.pop()
        # temp = deck.stack
        # remove = temp.pop(-1)
        # deck.stack = temp
        # print("removed", str(remove))
        print("after: ", str(len(deck.stack)))
        # deck.to_hand(me, numOfCardsPerPlayer)
        print("[DECK        ]: " + str(deck.size))
        # print("[DECK        ]: Deck has " + str(deck.size) + " cards.")

        _lock.release()
        # == Exiting the critical zone

        print_player(me, me.id)

        # Initialize keypress recorder
        try:
            global recorder
            recorder = Recorder.record(
                lambda event: me.key_handler(event, deck))
        except IOError as error:
            print("Could not initialize keypress recorder: " + repr(error))

        while recorder.is_recording:
            pass

    @staticmethod
    def cpu_process(playerList, turnList, deck, numOfCardsPerPlayer, _lock):
        import os
        print("Process ID:", os.getpid())

        cpu = Computer()
        playerList.append(cpu)

        # == Entering the critical zone
        _lock.acquire()

        deck.to_hand(cpu, numOfCardsPerPlayer)
        print("[DECK        ]: " + str(deck.size))
        
        _lock.release()
        # == Exiting the critical zone

        print_player(cpu, cpu.id)

    def winner_exists(self):
        """Checks if a winner exists

        Returns
        -------
        boolean
            A boolean that tells you if there is a winner
        """

        playersWithCards = [i for i, player in enumerate(
            self.players) if not player.hand.size == 0]

        if len(self.players) == 1:
            return True
        else:
            return False

    def scoreboard(self):
        """Prints scores (# of cards) of each player"""

        playersScores = [
            "Player {} has {} cards".format(i, player.hand.size)
            for i, player in enumerate(self.players)
        ]
        print_score("; ".join(playersScores))
