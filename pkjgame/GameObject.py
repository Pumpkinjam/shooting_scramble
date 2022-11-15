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
        