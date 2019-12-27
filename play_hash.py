from hash_game_env import *
from base_player import *
import time
import copy
import pickle
import random
import numpy as np
import os

NUM_EPOCHS = 100000
MAX_TRIES = 100
EXPLOIT_FACTOR = 0.30
VERBOSE = True

def random_play(state):
    copied_state = copy.deepcopy(state)
    return copied_state.step_randomly(HashGameState.PLAYER_0)

player = pickle.load(open(os.path.join('players', 'player_20000.pickle'), 'rb'))
    
game = HashGame()
all_possible_actions = game.possible_actions()

current_player = HashGameState.PLAYER_0

for epoch in range(NUM_EPOCHS):
    print('New game')

    game = HashGame()
    num_iterations = 0
    
    for tries in range(MAX_TRIES):
        try:
            game.render_state()
            
            if current_player == HashGameState.PLAYER_1:
                place_to_play = input('Where to play:')
                place_to_play = int(place_to_play)

                action = HashActions(play_at=place_to_play)
                game.play(current_player, action)
            else:
                next_action = player.best_action_for_state(game.current_state, random_play, verbose=True)
                game.play(HashGameState.PLAYER_0, next_action)

            reward = game.evaluate_state()

            if current_player == HashGameState.PLAYER_0:
                current_player = HashGameState.PLAYER_1
            else:
                current_player = HashGameState.PLAYER_0
            
            if reward == 20:
                game.render_state()
                print('Player 0 won')
                break
            elif reward == -20:
                game.render_state()
                print('Player 1 won')
                break
            elif game.draw():
                game.render_state()
                print('Draw')
                break
            num_iterations += 1

        except IndexError:
            break