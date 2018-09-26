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
import queue
import time

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
        # self.playerDict = 
        self.players = []
        self.turns = [queue.Queue(maxsize=1) for _ in range(numOfPlayers)]

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

        # # After every turn, check if winner exists
        # while not self.winner_exists():

        #     currentTurn = self.players[counter % self.numOfPlayers].id

        #     print("Turn " + str(counter))
        #     print_score(self)
        #     print(str(currentTurn) + "'s turn now.")

        #     self.turns.put(currentTurn)

        #     counter += 1

        #     time.sleep(2)

        # currentTurn = self.players[counter % self.numOfPlayers].id
        # print("Turn " + str(counter))
        # print(str(currentTurn) + "'s turn now.")
        # activate queue 
        self.turns[0].put(1)


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

        def check_if_turn_is_over():
            """ Player keeps spitting until turn is over.
            
            """

            if not deck.peek().value_ERS() == 0:
                # if the card that player put down is not face card, 
                # then continue to ask for more cards
                return True
            else: 
                # if card on top of stack is face card
                return False
            

        def key_handler(event):

            # if check_if_turn_is_over():
            #     # if turn is not over

            global recorder

            if isinstance(event, ke) and event.event == kes.DOWN:
            # Listen to only keyboard events

                if event.keyboard_key == kk.KEY_RIGHT_SHIFT:
                    # RIGHT SHIFT pressed -> player spits

                    me.spit(deck)
                    recorder.stop()
                    nextQueue.put(1)

                if event.keyboard_key == kk.KEY_LEFT_SHIFT:
                    # LEFT SHIFT pressed -> player slaps
                    # self.lock.acquire()

                    me.slap(deck)
                    recorder.stop()
                    nextQueue.put(1)

                    # self.lock.release()

                print_deck(deck)

            # else:
            #     # if turn is over, don't do anything even if keys pressed
            #     print("waiting on other players...")
            #     pass
        
        myQueue = self.turns[id]
        nextQueue = self.turns[(id+1)%self.numOfPlayers]

        while True:
            # time.sleep(1)
            # print("check queue in player process")

            try:

                whoseTurn = myQueue.get(timeout=3)
                print_turns(self)

                # print("It is " + str(whoseTurn) + "'s turn")
                # print(me.id)

                if whoseTurn:

                    # print("It is my turn!")
                    print("do player stuff")
                    # Initialize keypress recorder
                    try:
                        global recorder
                        recorder = Recorder.record(
                            lambda event: key_handler(event))
                    except IOError as error:
                        print(
                            "Could not initialize keypress recorder: " + repr(error))
                    
                    while recorder.is_recording:
                        pass

                    print("player stuff done")
                    

            except queue.Empty:
                print(".", end="")
                # print("queue is empty bc its not user's turn")

        # print_player(me, me.id)

        # == Exiting the critical zone

    # @staticmethod

    def cpu_process(self, id, deck):

        myQueue = self.turns[id]
        nextQueue = self.turns[(id+1)%self.numOfPlayers]

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
            # time.sleep(1)
            # print("check queue in cpu process")

            # print("cpu event set")
            # eventSet = cpuEvent.wait()

            try:

                whoseTurn = myQueue.get(timeout=3)
                print_turns(self)

                # print("It is " + str(whoseTurn) + "'s turn")
                # print(cpu.id)

                if whoseTurn:

                    # print("It is cpu's turn!")
                    # Initialize keypress recorder
                    
                    print("doing cpu stuff")
                    time.sleep(5)
                    print("cpu stuff done, added 1 to next queue")
                    nextQueue.put(1)

            except queue.Empty:
                print(".", end="")
                # print("queue is empty bc not cpu's turn")

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
