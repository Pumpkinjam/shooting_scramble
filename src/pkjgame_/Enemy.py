from AlarmManager import *
from Bullet import *
from Character import *
from Controller import *
from DisplayManager import *
from GameManager import *
from GameObject import *
from Gold import *
from Player import *
from Pos import *
from RoomManager import *
from SimpleDirection import *
from UserInfo import *

import random

class Enemy(Character):
    
    def __init__(self, room, id, x, y, width=16, height=16, image=None, dir=SimpleDirection.LEFT):
        super().__init__(room, id, x, y, width, height, image)
        #self.speed = self.room.speed
        self.dir = dir
        self.drop_rate = 0.9    # or else

    def __del__(self):
        # todo: motion for destructing
        if self.is_dropped():
            print('drop!')
            self.room.create_object(Gold, (self.x, self.y, DisplayManager.get_rectangle_image(Gold.size, Gold.size, (255,255,50,100)), self.dir))
            pass # generate gold, item, or else
            
    def destroy(self):
        self.room.del_object(self)
    
    def act(self, input_devices: tuple):
        self.move_by_dir(self.room.speed, self.dir)

        #print(self, self.center.is_left_than(Pos(0,0)))
        if self.center.is_left_than(Pos(0, 0)):
            self.destroy()

    def is_dropped(self):
        return random.random() < self.drop_rate