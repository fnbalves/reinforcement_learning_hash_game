from hash_game_env import *
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

WHERE_TO_SAVE = 10000

ALPHA = 0.1
GAMMA = 0.2

debug_num_failures = 0

growing_q_table = {}

def fetch_q(growing_q_table, state, action):
    try:
        return growing_q_table[state][action]
    except KeyError:
        return 0.0

def fetch_max_q(growing_q_table, state):
    try:
        return max(list(growing_q_table[state].values()))
    except:
        return 0.0

def update_value(growing_q_table, state, action, val):
    try:
        growing_q_table[state][action] = val
    except KeyError:
        growing_q_table[state] = {action: val}

def best_action_for_state(growing_q_table, state, player):
    try:
        action_to_do = max(growing_q_table[state], key=growing_q_table[state].get)
        return action_to_do
    except:
        copied_state = copy.deepcopy(state)
        return copied_state.step_randomly(player)

game = HashGame()
all_possible_actions = game.possible_actions()

current_player = HashGameState.PLAYER_0

for epoch in range(NUM_EPOCHS):
    game = HashGame()
    num_iterations = 0

    for tries in range(MAX_TRIES):
        try:
            if current_player == HashGameState.PLAYER_1:
                game.reverse_current_state()
                
            current_state = copy.deepcopy(game.current_state)
            
            if random.random() < EXPLOIT_FACTOR:
                next_action = game.current_state.step_randomly(HashGameState.PLAYER_0)
                next_state = copy.deepcopy(game.current_state)
            else:
                next_action = best_action_for_state(growing_q_table, current_state, HashGameState.PLAYER_0)
                game.play(HashGameState.PLAYER_0, next_action)
                next_state = copy.deepcopy(game.current_state)

            current_q = fetch_q(growing_q_table, current_state, next_action)
            next_max  = fetch_max_q(growing_q_table, next_state)
            reward = game.evaluate_state()
            #print('Current state', current_state)
            #print('Current q', current_q, 'Reward', reward)

            new_value = (1 - ALPHA)*current_q + ALPHA*(reward + GAMMA*next_max)
            #print('New value', new_value)

            update_value(growing_q_table, current_state, next_action, new_value)

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
                #if reward == -10:
                #    print('DRAW!!!!!!!!!!')
                break

            num_iterations += 1

        except:
            break

    if epoch % WHERE_TO_SAVE == 0:
        out = open(os.path.join('q_matrix', 'q_matrix_%d.pickle' % epoch), 'wb')
        pickle.dump(growing_q_table, out)
        out.close()

    print('Finished epoch %d with %d iterations' % (epoch, num_iterations))