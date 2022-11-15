from pkjgame import *

class Player(Character):

    weapon_list = []    # to be implemented (here, or maybe in other class)
    shield_list = []
    state_list = []
    
    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)
        #self.state
        #self.hp
        

    def move(self, x, y):
        self.center.move(x, y)
        
    def move_to(self, x, y):
        self.center.move_to(x, y)