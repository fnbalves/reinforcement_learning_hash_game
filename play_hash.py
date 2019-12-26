from hash_game_env import *
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

growing_q_table = pickle.load(open(os.path.join('q_matrix', 'q_matrix_120000.pickle'), 'rb'))

def fetch_q(growing_q_table, state, action):
    try:
        return growing_q_table[state][action]
    except KeyError:
        return 0.0

def fetch_max_q(growing_q_table, state, verbose=True):
    if verbose:
        for k in growing_q_table[state].keys():
            print('Action ', k, 'val ', growing_q_table[state][k])
    try:
        return max(list(growing_q_table[state].values()))
    except:
        return 0.0

def update_value(growing_q_table, state, action, val):
    try:
        growing_q_table[state][action] = val
    except KeyError:
        growing_q_table[state] = {action: val}

def best_action_for_state(growing_q_table, state, player, verbose=True):
    try:
        if verbose:
            for k in growing_q_table[state].keys():
                print('Action ', k, 'val ', growing_q_table[state][k])

        action_to_do = max(growing_q_table[state], key=growing_q_table[state].get)
        return action_to_do
    except:
        print('Played random')
        copied_state = copy.deepcopy(state)
        return copied_state.step_randomly(player)

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
                next_action = best_action_for_state(growing_q_table, game.current_state, current_player, verbose=VERBOSE)

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

        except:
            break