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

# Initialize lock to put around Deck object
lock = Lock()  # lock around accessing deck data


class ERS:

    def __init__(self, numOfPlayers):

        self.numOfPlayers = numOfPlayers
        self.numOfCardsPerPlayer = 52 // numOfPlayers
        self.players = []
        self.whoseTurn = []

        self.whoseTurn = [True] + ([False] * (numOfPlayers - 1))

    def __str__(self):

        playersScores = [
            "Player {} has {} cards".format(i, player.hand.size)
            for i, player in enumerate(game.players)
        ]

        return "; ".join(playersScores)

    def start_game(self):

        print_info("Game started!")

        # Initialize Deck
        deck = Deck()
        deck.shuffle()
        print_deck(deck)
        print(self.whoseTurn)

        # Initialize all players
        print_info(
            "Dealing {} cards each to {} players".format(
                self.numOfCardsPerPlayer, self.numOfPlayers
            )
        )
        # Initialize player 0 - fork subprocess

        # playerLock = Condition(lock)
        playerProcess = Thread(
            target=self.player_process,
            args=(self.players, self.whoseTurn, deck, self.numOfCardsPerPlayer, lock))

        playerProcess.start()

        # Initialize CPU's - fork subprocesses for CPU's
        listOfCPU = []
        for cpu_id in range(1, self.numOfPlayers):
            # CPU Processes
            # cpuLock = Condition(lock)
            cpuProcess = Thread(target=self.cpu_process,
                                args=(self.players, self.whoseTurn, deck, self.numOfCardsPerPlayer, lock))

            cpuProcess.start()
            listOfCPU.append(cpuProcess)

        for p in [playerProcess] + listOfCPU:
            p.join()

        print_score(self)

    def controller(self, deck):
        pass

    @staticmethod
    def player_process(playerList, turnList, deck, numOfCardsPerPlayer, _lock):
        import os

        me = User()
        playerList.append(me)

        # == Entering the critical zone
        _lock.acquire()

        deck.to_hand(me, numOfCardsPerPlayer)

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

        cpu = Computer()
        playerList.append(cpu)

        # == Entering the critical zone
        _lock.acquire()

        deck.to_hand(cpu, numOfCardsPerPlayer)

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
