#!/usr/bin/env python

'''
Author:     Alex Kim
Project:    Egyptian Rat Screw(ERS), Slap Game
File:       src/game.py
Purpose:    define game class

'''

from player import Player, Computer
from cards import Deck
from printer import *

from sneakysnek.recorder import Recorder
import sneakysnek.keyboard_event
import sneakysnek.keyboard_keys

class ERS:
    
    def __init__(self, numOfPlayers):
        self.numOfPlayers = numOfPlayers
        self.numOfCardsPerPlayer = 52 // numOfPlayers
        self.players = []

    def start_game(self):

        # Initialize deck
        print_info("Game started")
        deck = Deck()
        deck.shuffle()

        # Initialize all players
        print_info("Dealing {} cards each to {} players".format(self.numOfCardsPerPlayer, self.numOfPlayers))
        player = Player(0)
        deck.to_hand(player, self.numOfCardsPerPlayer)
        self.players.append(player)
        print_player(str(player), player.id)
        
        for cpu_id in range(1, self.numOfPlayers):

            cpu = Computer(cpu_id)
            deck.to_hand(cpu, self.numOfCardsPerPlayer)
            self.players.append(cpu)
            print_player(str(cpu), cpu.id)
        
        # Player will play as id=0
        me = self.players[0]
        
        def handler(event):

            global recorder

            if (isinstance(event, sneakysnek.keyboard_event.KeyboardEvent) and
                event.event == sneakysnek.keyboard_event.KeyboardEvents.DOWN):
                # print(event)

                # ESCAPE pressed -> escape program
                if event.keyboard_key == sneakysnek.keyboard_keys.KeyboardKey.KEY_ESCAPE:
                    print("Exiting program.")
                    recorder.stop()
                # RIGHT SHIFT pressed -> player spits
                if event.keyboard_key == sneakysnek.keyboard_keys.KeyboardKey.KEY_RIGHT_SHIFT:
                    me.spit(deck)
                    # TODO: Implement MYTURN
                    # if MYTURN:
                    #     me.spit(deck)
                    # else:
                    #     print_player("It's NOT your turn", me.id)
                # LEFT SHIFT pressed -> player slaps
                if event.keyboard_key == sneakysnek.keyboard_keys.KeyboardKey.KEY_LEFT_SHIFT:
                    me.slap(deck)
                
                print_deck(str(deck))
                print_player(str(me.hand), me.id)
                # self.scoreboard()

        try:        
            global recorder
            recorder = Recorder.record(handler)
        except IOError as error:
            print('Could not initialize keypress recorder: ' + repr(error))

        while recorder.is_recording:
            pass

    
    def winner_exists(self):
        """Checks if a winner exists
        
        Returns
        -------
        boolean
            A boolean that tells you if there is a winner
        """

        playersWithCards = [i for i, player in enumerate(self.players) if not player.hand.size == 0]

        if len(self.players) == 1:
            return True
        else:
            return False

    def scoreboard(self):
        """Prints scores (# of cards) of each player"""

        playersScores = ["Player {} has {} cards".format(i, player.hand.size) for i, player in enumerate(self.players)]
        print_score("; ".join(playersScores))