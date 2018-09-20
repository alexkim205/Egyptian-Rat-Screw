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
from sneakysnek.keyboard_event import KeyboardEvent as ke, KeyboardEvents as kes
from sneakysnek.keyboard_keys import KeyboardKey as kk


class ERS:

    def __init__(self, numOfPlayers):

        self.numOfPlayers = numOfPlayers
        self.numOfCardsPerPlayer = 52 // numOfPlayers
        self.playerDict = {}
        self.players = []

        # Initialize lock to put around Deck object
        self.lock = Lock()  # lock around accessing deck data

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

        # Initialize all players
        print_info(
            "Dealing {} cards each to {} players".format(
                self.numOfCardsPerPlayer, self.numOfPlayers
            )
        )

        listOfThreads = []

        # Initialize player 0 - fork subprocess
        user_id = 0
        playerProcess = Thread(
            target=self.player_process,
            args=(user_id, deck))

        listOfThreads.append(playerProcess)

        # Initialize CPU's - fork subprocesses for CPU's
        for cpu_id in range(1, self.numOfPlayers):

            # CPU Processes
            cpuProcess = Thread(target=self.cpu_process,
                                args=(cpu_id, deck))

            cpuProcess.start()
            listOfThreads.append(cpuProcess)

        for thread in listOfThreads:
            thread.start()
            thread.join()

        print_score(self)

    def controller(self, deck):
        pass

    # @staticmethod
    def player_process(self, id, deck):
        import os

        me = User(id)

        # == Entering the critical zone
        self.lock.acquire()

        self.playerDict[me.id] = [id, True]
        self.players.append(me)
        deck.to_hand(me, self.numOfCardsPerPlayer)

        self.lock.release()
        # == Exiting the critical zone

        print_player(me, me.id)

        # == Entering the critical zone
        self.lock.acquire()

        def key_handler(event):

            global recorder

            if isinstance(event, ke) and event.event == kes.DOWN:
                # Listen to only keyboard events

                if event.keyboard_key == kk.KEY_RIGHT_SHIFT:

                    if self.playerDict[me.id][1] == True:
                        # RIGHT SHIFT pressed -> player spits
                        me.spit(deck)
                    else:
                        print_player("It's not your turn!", me.id)

                if event.keyboard_key == kk.KEY_LEFT_SHIFT:
                    # LEFT SHIFT pressed -> player slaps
                    me.slap(deck)

                print_deck(deck)

        # Initialize keypress recorder
        try:
            global recorder
            recorder = Recorder.record(
                lambda event: key_handler(event))
        except IOError as error:
            print("Could not initialize keypress recorder: " + repr(error))

        while recorder.is_recording:
            pass
        
        self.lock.release()
        # == Exiting the critical zone

    # @staticmethod
    def cpu_process(self, id, deck):
        import os

        cpu = Computer(id)

        # == Entering the critical zone
        self.lock.acquire()

        # Append cpu: (int: index, bool: isTurn)
        self.playerDict[cpu.id] = [id, False]
        self.players.append(cpu)
        deck.to_hand(cpu, self.numOfCardsPerPlayer)

        self.lock.release()
        # == Exiting the critical zone

        print_player(cpu, cpu.id)

        # == Entering the critical zone
        self.lock.acquire()

        # Player loop, keep playing cards until winner exists
        # old_len = len(deck)
        while not self.winner_exists():

            # Trigger only after deck has been changed
            # (added or removed card)

            if self.playerDict[cpu.id][1] == True:
                # If player's turn
                while True:

                    cpu.delay_spit(deck)

                    if deck.peek().is_face():
                        # If player spits card and card is face card, \
                        # stop spitting and reset turns
                        next_index = (
                            self.playerDict[cpu.id][0] + 1) % len(self.playerDict)
                        self.playerDict[cpu.id][1] = False
                        self.playerDict[next_index] = True

                        break
            else:
                # If not player's turn, check if player can slap
                cpu.might_slap(deck)
        
        self.lock.release()
        # == Exiting the critical zone

    def winner_exists(self):
        """Checks if a winner exists

        Returns
        -------
        boolean
            A boolean that tells you if there is a winner
        """

        playersWithCards = [i for i, player in enumerate(
            self.players) if not player.hand.size == 0]

        if len(playersWithCards) == 1:
            return True
        else:
            return False
