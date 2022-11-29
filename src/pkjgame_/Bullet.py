from AlarmManager import *
from Bullet import *
from Character import *
from Controller import *
from DisplayManager import *
from Enemy import *
from GameManager import *
from GameObject import *
from Gold import *
from Player import *
from Pos import *
from RoomManager import *
from SimpleDirection import *
from UserInfo import *


class Bullet(GameObject):
    def __init__(self, room, id, x, y, width, height, image=None, speed=1, dir=SimpleDirection.RIGHT):
        super().__init__(room, id, x, y, width, height, image)
        self.speed = speed
        self.dir = dir
    
    '''
    def __del__(self):
        pass # add some effects?
'''
    
    def act(self, input_devices:tuple):
        self.move_by_dir(self.speed, self.dir)

        if (not self.is_in_room()):
            self.destroy()

        # wait, what...?
        for targ in list(self.room.objects.values()):
            
            if type(targ) == Enemy and self.check_collision(targ):
                print("Bullet hit!!")
                targ.destroy()
                self.destroy()