#!/usr/bin/env python

"""
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/game.py
Purpose:    define game class

"""

import ctypes

# from multiprocessing import Process, Condition, Lock, Queue
from threading import Lock, Thread, Event
import queue, time

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
        self.turns = queue.Queue()

        # Initialize lock to put around Deck object
        self.lock = Lock()  # lock around accessing deck data

        # Initialize event locks for each player thread
        # self.events = [Event() for _ in range(numOfPlayers)]
        self.threads = []

    def __str__(self):

        playersScores = [
            "Player {} has {} cards".format(i, player.hand.size)
            for i, player in enumerate(self.players)
        ]

        return "; ".join(playersScores)

    def ticker(self):
        counter = 0

        while not self.winner_exists():

            currentTurn = self.playerDict[counter % self.numOfPlayers][0]

            print("Turn " + str(counter))
            print_score(self)
            print(currentTurn + "'s turn now.")


            self.turns.put(currentTurn)

            counter += 1

            time.sleep(2)

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

        # Initialize player 0 - fork subprocess
        user_id = 0
        playerProcess = Thread(
            target=self.player_process,
            args=(user_id, deck))

        self.threads.append(playerProcess)

        # Initialize CPU's - fork subprocesses for CPU's
        for cpu_id in range(1, self.numOfPlayers):

            # CPU Processes
            cpuProcess = Thread(target=self.cpu_process,
                                args=(cpu_id, deck))

            self.threads.append(cpuProcess)

        # for event in self.events:
        #     event.set() # set each event
        # set player event
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

        # Start game ticker to set turns
        self.ticker()

        print_score(self)

    def controller(self, deck):
        pass

    # @staticmethod
    def player_process(self, id, deck):
        import os

        me = User(id)

        # == Entering the critical zone
        # self.lock.acquire()

        # playerEvent = self.events[id]

        self.playerDict[id] = [me.id, True]
        self.players.append(me)
        deck.to_hand(me, self.numOfCardsPerPlayer)

        def key_handler(event):

            global recorder

            if isinstance(event, ke) and event.event == kes.DOWN:
                # Listen to only keyboard events

                if event.keyboard_key == kk.KEY_RIGHT_SHIFT:
                    # RIGHT SHIFT pressed -> player spits

                    if self.playerDict[me.id][1] == True:
                        me.spit(deck)
                    else:
                        print_player("It's not your turn!", me.id)

                if event.keyboard_key == kk.KEY_LEFT_SHIFT:
                    # LEFT SHIFT pressed -> player slaps
                    # self.lock.acquire()

                    me.slap(deck)

                    # self.lock.release()

                print_deck(deck)

        while True:
            try:
                whoseTurn = self.turns.get(timeout=3)
            except queue.Empty:
                print("queue is empty")
                return
            if whoseTurn == me.id:

                print("It is my turn!")
                # Initialize keypress recorder
                try:
                    global recorder
                    recorder = Recorder.record(
                        lambda event: key_handler(event))
                except IOError as error:
                    print("Could not initialize keypress recorder: " + repr(error))

                while recorder.is_recording:
                    pass

            else:
                print("It is NOT my turn!")

        # print_player(me, me.id)

        # == Exiting the critical zone

    # @staticmethod
    def cpu_process(self, id, deck):
        import os

        cpu = Computer(id)

        # == Entering the critical zone
        # self.lock.acquire()

        # Append cpu: (int: index, bool: isTurn)
        self.playerDict[id] = [cpu.id, False]
        self.players.append(cpu)
        deck.to_hand(cpu, self.numOfCardsPerPlayer)

        # self.lock.release()
        # == Exiting the critical zone

        print_player(cpu, cpu.id)

        # cpuEvent = self.events[id]

        # Player loop, keep playing cards until winner exists
        # old_len = len(deck)

        while True:

            # print("cpu event set")
            # eventSet = cpuEvent.wait()

            try:
                whoseTurn = self.turns.get(timeout=3)
                print("It is " + whoseTurn + "'s turn")
            except queue.Empty:
                print("queue is empty")
                return

            if whoseTurn == cpu.id:

                print("It is cpu's turn!")
                # Initialize keypress recorder


            else:
                print("It is NOT my turn!")

                # self.lock.acquire()

                # cpu.delay_spit(deck)

                # if deck.peek().is_face():
                #         # If player spits card and card is face card, \
                #         # stop spitting and reset turns
                #     next_index = (
                #         self.playerDict[cpu.id][0] + 1) % len(self.playerDict)
                #     self.playerDict[cpu.id][1] = False
                #     self.playerDict[next_index] = True

                #     # self.lock.release()

                #     break

                #     # self.lock.release()
                # else:
                #     # If not player's turn, check if player can slap
                #     # self.lock.acquire()

                #     cpu.might_slap(deck)

                #     # self.lock.release()

            # Trigger only after deck has been changed
            # (added or removed card)

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
