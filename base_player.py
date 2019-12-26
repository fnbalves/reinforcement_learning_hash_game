class BaseTablePlayer:
    def __init__(self):
        self.growing_q_table = {}

    def fetch_q(self, state, action):
        try:
            return self.growing_q_table[state][action]
        except KeyError:
            return 0.0
    
    def fetch_max_q(self, state):
        try:
            return max(list(self.growing_q_table[state].values()))
        except:
            return 0.0
    
    def update_q_value(self, action, val):
        try:
            self.growing_q_table[state][action] = val
        except KeyError:
            self.growing_q_table[state] = {action: val}
    
    def best_action_for_state(state, default_action):
        
