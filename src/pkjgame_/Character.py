from AlarmManager import *
from Bullet import *
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

# All Characters (Player, Enemy) must be extended by this class
class Character(GameObject):
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super().__init__(room, id, x, y, width, height, image)