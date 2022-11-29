from GameManager import *
from GameObject import *
from Player import *
from Pos import *
from RoomManager import *
from SimpleDirection import *
from UserInfo import *

class Gold(GameObject):
    size = 8
    def __init__(self, room, id, x, y, image=None, dir=None):
        # actually, speed and dir must not be None
        super().__init__(room, id, x, y, Gold.size, Gold.size, image)
        self.dir = dir
    
    def __del__(self):
        print("gold get!")

    def act(self, _):
        self.move_by_dir(self.room.speed, self.dir)

        if self.center.is_left_than(Pos(0, 0)):
            self.destroy()
        
        if self.check_collision(self.room.obj_player):
            print("gold++;")
            self.destroy()