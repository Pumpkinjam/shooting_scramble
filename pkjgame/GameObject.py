from pkjgame import *

from abc import *
from PIL import Image
import numpy as np

# All Objects in game (Character, Item, Bullets...) must be extended by this class
# This class is abstract (Interface-like)
class GameObject(metaclass=ABCMeta):
    '''
    * GameObject must have...
    
    Image img;
    String state
    Pos center
    '''

    @abstractmethod
    def __init__(self, room, id, x, y, width, height, image=None):
        if image is not None:
            self.img = image
        else:
            self.img = Image.new("RGBA", (width, height))
        
        self.room = room
        self.id = id
        self.state = None
        self.center = Pos(x, y)
        self.x = x
        self.y = y
        self.outline = "#FFFFFF"

    @abstractmethod
    def act(self, input_devices: tuple):
        pass

    # if dir is not None, arguments x and y will be ignored
    def move(self, x=0, y=0):
        self.center.move(x, y)
        self.x = self.center.x
        self.y = self.center.y

    def move_by_dir(self, speed, dir):
        if dir == Direction.RIGHT:
            self.move(speed, 0)
        elif dir == Direction.LEFT:
            self.move(-speed, 0)
        elif dir == Direction.UP:
            self.move(0, -speed)
        elif dir == Direction.DOWN:
            self.move(0, speed)
        else:
            raise Exception('Unknown direction')
        
    def move_to(self, x, y):
        self.center.move_to(x, y)
        self.x = self.center.x
        self.y = self.center.y
    
    def get_range(self) -> tuple:   # (Pos1, Pos2)
        return (Pos(self.x - self.width/2, self.y - self.height/2), Pos(self.x + self.width/2, self.y + self.height/2))
    
    def is_in_range(self, ran: tuple):
        lt = ran[0]; rb = ran[1]
        return (lt.x < self.x < rb.x and lt.y < self.y < rb.y)

    def check_collision(self, other):
        return self.is_in_range(other.get_range())
    
    def set_img(self, img):
        self.img = img