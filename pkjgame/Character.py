from pkjgame import *

# All Characters (Player, Enemy) must be extended by this class
class Character(GameObject):

    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)
                