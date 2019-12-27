from hash_game_env import *
from base_player import *

import time
import copy
import pickle
import random
import numpy as np
import os

NUM_EPOCHS = 1000000
MAX_TRIES = 100
EXPLOIT_FACTOR = 0.30
VERBOSE = False
VISUAL_DELAY = 0

NUM_EPOCH_TO_SAVE = 10000

ALPHA = 0.1
GAMMA = 0.2

debug_num_failures = 0

def random_play(state):
    copied_state = copy.deepcopy(state)
    return copied_state.step_randomly(HashGameState.PLAYER_0)

player = BaseTablePlayer()

game = HashGame()
all_possible_actions = game.possible_actions()

current_player = HashGameState.PLAYER_0

for epoch in range(NUM_EPOCHS):
    game = HashGame()
    num_iterations = 0

    latest_state = None
    latest_action = None
    latest_reward = None

    for tries in range(MAX_TRIES):
        try:
            if current_player == HashGameState.PLAYER_1:
                game.reverse_current_state()
                
            current_state = copy.deepcopy(game.current_state)
            
            if random.random() < EXPLOIT_FACTOR:
                next_action = game.current_state.step_randomly(HashGameState.PLAYER_0)
                next_state = copy.deepcopy(game.current_state)
            else:
                next_action = player.best_action_for_state(current_state, random_play)
                game.play(HashGameState.PLAYER_0, next_action)
                next_state = copy.deepcopy(game.current_state)

            if latest_state is not None:
                current_q = player.fetch_q(latest_state, latest_action)
                next_max  = player.fetch_max_q(current_state)
                reward = game.evaluate_state()
                
                new_value = (1 - ALPHA)*current_q + ALPHA*((latest_reward - reward) + GAMMA*next_max)
                
                player.update_q_value(latest_state, latest_action, new_value)
            else:
                current_q = player.fetch_q(current_state, next_action)
                next_max  = player.fetch_max_q(next_state)

                reward = game.evaluate_state()
            
                new_value = (1 - ALPHA)*current_q + ALPHA*(reward + GAMMA*next_max)
            
                player.update_q_value(current_state, next_action, new_value)

            latest_reward = reward
            latest_state = current_state
            latest_action = next_action

            if current_player == HashGameState.PLAYER_1:
                game.reverse_current_state()
                
            if VERBOSE:
                game.render_state()
                print('--------------')
                time.sleep(VISUAL_DELAY)

            if current_player == HashGameState.PLAYER_0:
                current_player = HashGameState.PLAYER_1
            else:
                current_player = HashGameState.PLAYER_0
            
            if reward == 20 or reward == -20:
                break

            num_iterations += 1

        except IndexError:
            break

    if epoch % NUM_EPOCH_TO_SAVE == 0:
        out = open(os.path.join('players', 'player_%d.pickle' % epoch), 'wb')
        pickle.dump(player, out)
        out.close()

    print('Finished epoch %d with %d iterations' % (epoch, num_iterations))