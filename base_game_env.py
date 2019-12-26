import random
from abc import abstractmethod

class BaseGameState:

    def __init__(self,  state=None, seed=None):
        if seed is not None:
            random.seed(seed)

        if state is not None:
            self.state = state
        else:
            self.state = self.initial_state()

    @abstractmethod
    def step_randomly(self, current_player):
        """Implement this method to define how a random play should be done"""
        
    @abstractmethod
    def initial_state(self):
        """Implement this method to define the initial state of the game"""

    def __hash__(self):
        return hash(tuple(self.state))
    
    def __eq__(self, other):
        return hash(tuple(self.state)) == hash(tuple(other.state))

    def __repr__(self):
        return str(self.state)

class BaseGame:
    def __init__(self, state_class, initial_state = None):
        if initial_state is not None:
            self.current_state = initial_state
        else:
            self.current_state = state_class()

    @abstractmethod
    def possible_actions(self):
        """Implement this method to define the possible actions of the game"""

    @abstractmethod
    def render_state(self):
        """Implement this method to define how a game state should be displayed at the screen"""
    
    @abstractmethod
    def play(self, current_player, action):
        """Implement this method to define how a certain action is played at the game. Remember to implement an action class"""

    @abstractmethod
    def reverse_current_state(self):
        """Implement this method to define how the game state should be reversed to represent the situation of oposing players"""

    @abstractmethod       
    def evaluate_state(self):
        """Implement this method to define how to evaluate how good a game state is (for Q-learning), It is 
        interesting to always look at the perspective of the same player. Use the reverse_current_state during
        training"""

