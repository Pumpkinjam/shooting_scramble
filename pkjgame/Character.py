from pkjgame import *

# All Characters (Player, Enemy) must be extended by this class
class Character(GameObject):

    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)

    def move(self, x, y):
        self.center.move(x, y)
        
    def move_to(self, x, y):
        self.center.move_to(x, y)
                