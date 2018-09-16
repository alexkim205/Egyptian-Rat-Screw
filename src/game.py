#!/usr/bin/env python

"""
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/game.py
Purpose:    define game class

"""

from multiprocessing import Process, Condition, Lock

from player import Player, Computer
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
        self.whoseTurn = [True] + ([False] * (numOfPlayers - 1))

    def start_game(self):

        print_info("Game started!")

        gameManager = GameManager()
        gameManager.start()

        # Initialize Deck
        deck = gameManager.Deck()
        deck.shuffle()

        # Initialize all players
        print_info(
            "Dealing {} cards each to {} players".format(
                self.numOfCardsPerPlayer, self.numOfPlayers
            )
        )
        # Initialize player 0 - fork subprocess
        me = gameManager.User()
        deck.to_hand(me, self.numOfCardsPerPlayer)
        self.players.append(me)

        playerLock = Condition(lock)
        playerProcess = Process(
            target=self.player_process, args=(me, deck, playerLock, lock))
        print_player(str(me), me.id)

        playerProcess.start()

        # Initialize CPU's - fork subprocesses for CPU's
        listOfCPU = []
        for cpu_id in range(1, self.numOfPlayers):
            cpu = gameManager.Computer(cpu_id)
            deck.to_hand(cpu, self.numOfCardsPerPlayer)
            self.players.append(cpu)

            # CPU Processes
            cpuLock = Condition(lock)
            cpuProcess = Process(target=self.cpu_process,
                                 args=(cpu, deck, cpuLock, lock))

            print_player(str(cpu), cpu.id)

            cpuProcess.start()
            listOfCPU.append(cpuProcess)

        print("Main program continues")

        for p in [playerProcess] + listOfCPU: p.join()


    def controller(self, deck):
        pass

    @staticmethod
    def player_process(player, deck, _playerLock, _lock):
        import os
        print("Process ID:", os.getpid())

        _lock.acquire()
        print(player)

        # Initialize keypress recorder
        try:
            global recorder
            recorder = Recorder.record(lambda event: player.handler(event, deck))
        except IOError as error:
            print("Could not initialize keypress recorder: " + repr(error))

        while recorder.is_recording:
            pass

        # print(deck)
        _lock.release()

    @staticmethod
    def cpu_process(computer, deck, _cpuLock, _lock):
        import os
        print("Process ID:", os.getpid())

        _lock.acquire()
        print(computer.hand)
        _lock.release()

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
