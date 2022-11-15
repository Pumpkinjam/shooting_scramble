from pkjgame import *

import random as r

class Enemy(Character):
    
    def __init__(self, x, y, width, height, image=None):
        super.__init__(x, y, width, height, image)
        self.drop_rate = 0.3    # or else

    def __del__(self):
        # motion for destructing
        if r.random() < self.drop_rate:
            pass # generate gold, item, or else

    def move(self, x, y):
        self.center.move(x, y)
        
    def move_to(self, x, y):
        self.center.move_to(x, y)