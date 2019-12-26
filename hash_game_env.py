import random
from base_game_env import *

class HashActions:
    def __init__(self, play_at):
        self.play_at = play_at

    def __hash__(self):
        return self.play_at

    def __eq__(self, other):
        return self.play_at == other.play_at

    def __repr__(self):
        return str(self.play_at)

class HashGameState(BaseGameState):
    EMPTY = 1
    PLAYER_0 = 2
    PLAYER_1 = 3

    def __init__(self, states=None, seed=None):
        super().__init__(states, seed)

    @staticmethod
    def fetch_random(max_num):
        return int(max_num*random.random())

    def step_randomly(self, current_player):
        empty_houses = [i for i, x in enumerate(self.state) if x == HashGameState.EMPTY]
        num_empty_houses = len(empty_houses)
        index_to_fetch = HashGameState.fetch_random(num_empty_houses)
        
        house_to_fill = empty_houses[index_to_fetch]
        self.state[house_to_fill] = current_player
        return HashActions(play_at=house_to_fill)
        
    def initial_state(self):
        return [1]*9

class HashGame(BaseGame):
    EVALUATION_LINES = [[0,1,2], [3,4,5], [6,7,8],
                        [0,3,6], [1,4,7], [2,5,8],
                        [0,4,8], [2,4,6]]

    def __init__(self, initial_state = None):
        super().__init__(HashGameState, initial_state)
    
    def possible_actions(self):
        all_actions = []
        for i in range(9):
            all_actions.append(HashActions(i))
        return all_actions

    def is_action_possible(self, action):
        return self.current_state.state[action.play_at] == HashGameState.EMPTY

    def __elements_in_line(self, line):
        elems = []
        for L in line:
            elems.append(self.current_state.state[L])
        return list(set(elems))

    def better_situation_player(self, player):
        max_elems = -1
        for line in HashGame.EVALUATION_LINES:
            elems = self.__elements_in_line(line)
            num_match = len([k for k in elems if k == player])
            
            if max_elems < num_match:
                max_elems = num_match
        return max_elems

    def player_0_won(self):
        for line in HashGame.EVALUATION_LINES:
            elems = self.__elements_in_line(line)
            if len(elems) == 1 and elems[0] == HashGameState.PLAYER_0:
                return True
        return False

    def player_1_won(self):
        for line in HashGame.EVALUATION_LINES:
            elems = self.__elements_in_line(line)
            if len(elems) == 1 and elems[0] == HashGameState.PLAYER_1:
                return True
        return False

    def draw(self):
        all_filled = not (HashGameState.EMPTY in self.current_state.state)
        return all_filled and (not self.player_0_won()) and (not self.player_1_won())
    
    def render_state(self):
        current_house = 0
        for i in range(3):
            str_to_print = '|'
            for j in range(3):
                char_to_add = ' '
                current_s = self.current_state.state[current_house]
                if current_s == HashGameState.PLAYER_0:
                    char_to_add = 'O'
                elif current_s == HashGameState.PLAYER_1:
                    char_to_add = 'X'

                str_to_print += '%c|' % char_to_add

                current_house += 1
            print(str_to_print)
        
    def play(self, current_player, action):
        self.current_state.state[action.play_at] = current_player

    def reverse_current_state(self):
        for i, h in enumerate(self.current_state.state):
            if h == HashGameState.PLAYER_0:
                self.current_state.state[i] = HashGameState.PLAYER_1
            elif h == HashGameState.PLAYER_1:
                self.current_state.state[i] = HashGameState.PLAYER_0
            
    def evaluate_state(self):
        if self.player_0_won():
            return 20
        elif self.player_1_won():
            return -20
        else:
            return self.better_situation_player(HashGameState.PLAYER_0)

