from pkjgame import *

import random as r

class Enemy(Character):
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super.__init__(room, id, x, y, width, height, image)
        self.drop_rate = 0.3    # or else

    def __del__(self):
        # motion for destructing
        import random as r
        if r.random() < self.drop_rate:
            pass # generate gold, item, or else
    
    def act(self, input_devices: tuple):
        pass