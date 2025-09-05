import random

class RandomAgent:
    def __init__(self, env):
        self.env = env

    def get_action(self):
        return self.env.action_space.sample()

class RandomAgentWithCustomMoves:
    def __init__(self, env, custom_moves):
        self.env = env
        #self.actions = [ [[idx], [0]] for idx in range(9)]
        self.actions = [[[7, 6, 5], [0, 0, 2]]]
        #self.actions = [[[7], [0]]]
        for action in self.actions:
            assert len(action[0]) == len(action[1]), "The number of moves and the attacks must be the same"

        self.executing_action = False
        self.execution_idx = 0
        self.selected_action = [[0], [0]]

    def get_action(self):
        action_to_execute = [0, 0]
        if not self.executing_action:
            # Randomly select an action from the list of actions
            self.selected_action = self.actions[random.randint(0, len(self.actions) - 1)]

            if len(self.selected_action[0]) > 1:
                self.executing_action = True
            action_to_execute = [self.selected_action[0][self.execution_idx], self.selected_action[1][self.execution_idx]]
        else:
            self.execution_idx += 1
            action_to_execute = [self.selected_action[0][self.execution_idx], self.selected_action[1][self.execution_idx]]
            if self.execution_idx == (len(self.selected_action[0]) - 1):
                self.executing_action = False
                self.execution_idx = 0

        return action_to_execute