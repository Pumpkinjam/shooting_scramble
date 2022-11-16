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
    def __init__(self, id, x, y, width, height, image=None):
        if image is not None:
            self.img = image
        else:
            self.img = Image.new("RGBA", (x,y))
        
        self.id = id
        self.state = None
        self.center = Pos(x, y)
        self.outline = "#FFFFFF"

    @abstractmethod
    def move(self, x, y):
        self.center.move(x, y)
        
    @abstractmethod
    def move_to(self, x, y):
        self.center.move_to(x, y)
    
    def get_range(self) -> tuple:   # (Pos1, Pos2)
        return (Pos(self.x - self.width/2, self.y - self.height/2), Pos(self.x + self.width/2, self.y + self.height/2))
    
    def is_in_range(self, ran: tuple):
        lt = ran[0]; rb = ran[1]
        return (lt.x < self.x < rb.x and lt.y < self.y < rb.y)

    def check_collision(self, other: GameObject):
        return self.is_in_range(other.get_range())
