import random
ACTIONS = ['nop', 'rotate', 'down', 'left', 'right', 'drop']

class Player:
    def __init__(self, name):
        self.name = name
    
    def act(self, info):
        return random.choice(ACTIONS)

