#!/usr/bin/env python
# coding: utf-8

# In[4]:


#!/usr/bin/env python
# coding: utf-8

#The rules of Pig are simple. The game features two players, whose goal is to reach 100 points first. Each
#turn, a player repeatedly rolls a die until either a 1 is rolled or the player holds and scores the sum of the
#rolls (i.e. the turn total)

import random
import sys
import os
import argparse
import time

# Create a class named "Player" for storing player's info 
class Player(object):

    def __init__(self):
        self.score = 0
        self.turn = False
        self.set_name()
        self.type = 'human'
        self.pending_points = 0

    def get_score(self):
        return self.score

    def set_score(self, points):
        self.score += points

    def get_name(self):
        return self.name

    #Set player name for human players 
    def set_name(self):
        
        while True:
            try:
                new_name = raw_input('Enter player name: ').strip()
                self.name = new_name
                break
            except ValueError:
                print ('please enter a string')
                continue

    def set_turn(self, turn):
        self.turn = turn

    def get_turn(self):
        return self.turn

    def get_type(self):
        return self.type

    def set_pending_points(self, points):
        self.pending_points += points

    def reset_pending_points(self):
        self.pending_points = 0

    def get_pending_points(self):
        return self.pending_points

    def get_choice(self):
        while True:
            try:
                player_choice = raw_input("Please enter [h] for hold, or [r] for roll: ").strip()
                if player_choice.lower() == 'h':
                    return True
                elif player_choice.lower() == 'r':
                    return False
                else:
                    print ('Invalid entry, please enter [h] for hold or [r] for roll')
            except ValueError:
                print ('Entry must be of string data type')

# Class for CPU type player 
class Computer(Player):
    def __init__(self):
        Player.__init__(self)
        self.type = 'computer'

    def get_choice(self):
        return int(self.get_pending_points()) >= 25 or (int(self.get_score()) - 100) >= 25

    def set_name(self):
        self.name = 'computer {}'.format(random.randint(1, 30))

# Class for creating players of either human or CPU type
class PlayerFactory(object):
    def player_type(self, ptype):
        if ptype == 'human':
            return Player()
        elif ptype == 'computer':
            return Computer()

# Create a class for storing dice details
class Dice(object):
    def __init__(self):
        self.value = random.seed(0)

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

    def get_roll(self):
        return self.value

# Game class for holding player objects, pending points and running total per turn as well as roll data
class Game(object):
    def __init__(self):
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []

    # Function for adding new player to the game
    def add_player(self, ptype=str, index=int):
        player_factory = PlayerFactory()
        if ptype == 'computer':
            self.game_data.append(player_factory.player_type("computer"))
            self.score_data[self.game_data[index].get_name()] = self.game_data[index].get_score()
        elif ptype == 'human':
            self.game_data.append(player_factory.player_type("human"))
            self.score_data[self.game_data[index].get_name()] = self.game_data[index].get_score()

    # Function for adding multiple players 
    def add_players_to_game(self, players):
        for player in range(players):
            self.add_player(player)

    def get_active_player(self):
        return self.game_data[self.active_player]

    # Function to check current player scores in relation to the winning score of 100 
    def get_win_state(self):
        for player in self.game_data:
            if player.get_score() >= 100:
                return True
        return False
    
    # Function for game status 
    def get_game_status(self):
        os.system('cls')
        print ('Pig Game\n')
        print('{:15} : {:>6}\n').format('Player', 'Score')
        for player in self.game_data:
            print('{:15} : {:6} \n').format(player.get_name(), player.get_score())
        print('{} is rolling').format(self.get_active_player().get_name())
        if self.dice.get_roll() == 1:
            print('The last score was {}, next player\'s turn!').format(self.dice.get_roll())
        else:
            print('The last score was {}').format(self.dice.get_roll())
        print('Pending Points: {:>10}').format(self.get_active_player().get_pending_points())
    
    # Function for tracking human player turns
    def player_turn(self):
        rolling = self.get_active_player()
        rolling.set_turn(True)
        self.get_game_status()
        while rolling.get_turn() and not self.get_win_state():
            rollorhold = rolling.get_choice()
            if rollorhold:
                rolling.set_score(rolling.get_pending_points())
                rolling.reset_pending_points()
                rolling.set_turn(False)
            else:
                roll = self.dice.roll()
                if roll == 1:
                    rolling.reset_pending_points()
                    rolling.set_turn(False)
                rolling.set_pending_points(roll)
                self.get_game_status()
                continue

    # Function for setting up the players and type and keeping track of game status
    def game_loop(self, player1, player2, num_players=2):
        if num_players <= 2:
            self.add_player(player1, 0)
            self.add_player(player2, 1)
        elif num_players > 2:
            for player in range(2, num_players):
                self.add_players_to_game(player)

        while not self.get_win_state():
            for player in self.game_data:
                self.active_player = (self.turns % len(self.game_data))
                self.player_turn()
                self.turns += 1

        for player in self.game_data:
            self.score_data[player.get_name()] = player.get_score()
        scores = list(self.score_data.values())
        players = list(self.score_data.keys())
        top_score = max(scores)
        winner = players[scores.index(max(scores))]
        print('\nThe winner is  {} with {} points').format(winner, top_score)
        self.reset_game()

    # Function to reset game variables when a new game is selected
    def reset_game(self):
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []

    # Function to implement game restart when selected 
    def restart_game(self, player1, player2, num_players):
        while True:
            try:
                new_game = raw_input("\nPlay again? [y]|[n]: ").strip()
                if new_game == 'y':
                    self.game_loop(player1, player2, num_players)
                elif new_game == 'n':
                    print ('Thank you for playing')
                    sys.exit()
            except ValueError:
                continue

# Class for a 60 second timed version of the game 
class TimedGameProxy(Game):
    def __init__(self):
        Game.__init__(self)
        self.start_time = time.time()
        self.end_time = time.time() + 60
    
    # Function to check win state based on score and time 
    def get_win_state(self):
        if time.time() >= self.end_time:
            return True
        for player in self.game_data:
            if player.get_score() >= 100:
                return True
        return False

    def get_time_remaining(self):
        return self.end_time - time.time()

    def get_game_status(self):
        os.system('cls')
        print ('Pig Game\n')
        print('{:15} : {:>6}\n').format('Player', 'Score')
        for player in self.game_data:
            print('{:15} : {:6} \n').format(player.get_name(), player.get_score())
        print('{} is rolling').format(self.get_active_player().get_name())
        if self.dice.get_roll() == 1:
            print('The last score was {}, next player\'s turn').format(self.dice.get_roll())
        else:
            print('The last score was {}').format(self.dice.get_roll())
        print('Pending Points: {:>10}').format(self.get_active_player().get_pending_points())
        print('Time Remaining: {} seconds').format(round(self.get_time_remaining()))

    def reset_game(self):
        self.active_player = 0
        self.turns = 0
        self.dice = Dice()
        self.score_data = {}
        self.game_data = []
        self.start_time = time.time()
        self.end_time = time.time() + 60

# Main method to run the application 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_players',
                        help='Number of players in our game',
                        type=int, required=False, default=2)
    parser.add_argument('--player1', type=str.lower,
                        choices=['human', 'computer'], default='human', required=False)
    parser.add_argument('--player2', type=str.lower,
                        choices=['human', 'computer'], default='computer', required=False)
    parser.add_argument('--timed', help='Determine if the game is timed',
                        choices=['yes', 'no'], required=False, default='no', type=str.lower)
    args = parser.parse_args()
    if args.timed.lower() == "yes":
        new_game = TimedGameProxy()
    elif args.timed.lower() == "no":
        new_game = Game()
    new_game.game_loop(args.player1, args.player2, args.num_players)
    new_game.restart_game(args.player1, args.player2, args.num_players)


if __name__ == '__main__':
    main()


# In[ ]:




