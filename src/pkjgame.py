import time
from abc import *
import numpy as np
from math import sqrt
import csv

from PIL import Image, ImageDraw, ImageFont

import board
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789

class Pos:
    '''
    float x, y;
    '''

    def __init__(self, x, y):
        self.x = x; self.y = y

    def at_same_position_to(self, other):
        return (self.x == other.x and self.y == other.y)
    
    def is_left_than(self, other):
        return self.x < other.x
    
    def is_right_than(self, other):
        return self.x > other.x

    def is_above_than(self, other):
        return self.y < other.y
    
    def is_below_than(self, other):
        return self.y > other.y
    
    def move_to(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def move(self, x, y):
        self.x += x
        self.y += y
    
    def distance_to(self, other) -> float:
        return sqrt(self.x * self.x + self.y * self.y)
    
    def to_tuple(self) -> tuple:
        return (self.x, self.y)
    
    def to_string(self) -> str:
        return f'[Pos ({self.x}, {self.y})]'


class Alarm:
    '''
    float clock; // once Alarm have been done, clock becomes -1
    float start_time;
    float timing;

    int id;
    '''
    def __init__(self, id, clock):
        self.id = id
        self.clock = clock
        self.start_time = time.time()
        self.timing = self.start_time + self.clock
    
    # return if the valid alarm was done
    def isDone(self) -> bool:
        if self.clock == -1: return False

        if (time.time() > self.timing):
            self.clock = -1
            return True
        else:
            return False
    

    def getPassedTime(self) -> float:
        if self.clock == -1.: return -1.

        tmp = self.timing - time.time()
        if tmp < 0: return -1.
        else: return tmp
        
    
    # reset the start_time and clock (with new_clock)
    def setClock(self, new_clock) -> None:
        self.start_time = time.time()
        self.clock = new_clock
        self.timing = self.start_time + self.clock
    
    # if alarm is done, set Alarm with new_clock and return True
    # else, return False
    def resetAlarm(self, new_clock=None) -> bool:
        if not self.isDone(): return False;

        self.started_time = time.time()
        if new_clock is not None: 
          self.clock = new_clock

        return True


class AlarmManager:
    current_id = 0  # primary key for alarms

    def __init__(self):
        self.alarms = dict()
        # self.threads = dict()
    
    def new(self, t=-1): return self.new_alarm(t)
    def new_alarm(self, t=-1) -> Alarm:
        AlarmManager.current_id += 1
        return self._new_alarm(AlarmManager.current_id, t)

    def is_done(self, obj_alarm: Alarm) -> bool:
        try:
            return self.alarms[obj_alarm.id].isDone()
        except:
            print('that alarm does not belong to this manager.')
            return None

    def delete(self, obj_alarm: Alarm) -> None:
        obj_alarm.stop()
        del self.alarms[obj_alarm.id]
    
    # do not to call this function directly from the outside of the class
    def _new_alarm(self, id, t) -> Alarm:
        self.alarms[id] = Alarm(id, t)
        return self.alarms[id]

    def get_alarm_list(self) -> list:
        return [_ for _ in self.alarms.values()]



class DisplayManager:

    bg_length = 240

    def __init__(self, obj_list=None):
        # basic fields
        self.objects = tuple()
        self.width = DisplayManager.bg_length
        self.height = DisplayManager.bg_length

        # hardware connections
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000 * 1000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    width=self.width,
                    height=self.height,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # fields initialization
        # these are updated by refreshing
        self.bg = Image.new("RGBA", (self.width, self.height))
        self.paper = self.bg.copy()
          #self.pen = ImageDraw.Draw(self.paper)

        self.refresh(obj_list)

    def refresh(self, obj_list=None):
        self.paper = self.bg.copy()
        if obj_list is not None:
            self.objects = obj_list
        
        for obj in self.objects:
            if not isinstance(obj, GameObject):
                print('Something went wrong...')
                print(type(obj))
                print(obj)
            else:
                self.paper.paste(obj.img, obj.center.to_tuple())
        
          #self.pen = ImageDraw.Draw(self.paper)
        self.display()
    
    def set_background(self, fill: tuple):
        ImageDraw.Draw(self.bg).rectangle((0, 0, self.width, self.height), fill)    # bg becomes new background
        self.refresh(self.objects)  # update!
    
    def display(self):
        self.disp.image(self.paper)

    @staticmethod
    def get_rectangle_image(width: int, height: int, color: tuple):
        rec = Image.new('RGBA', (width, height))
        ImageDraw.Draw(rec).rectangle((0, 0, 32, 32), fill=color)
        return rec


class GameManager:

    def __init__(self, fps, screen_width, screen_height):
        self.fps = fps
        self.spf = 1/fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.object_id = 0

        self.objects = dict()       # keys: id (int), values: obj (GameObject)
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.user = UserInfo()

        self.dm.set_background((255, 255, 255, 100))
        self.fps_alarm = self.am.new_alarm(self.spf)

        self.setup()
        self.manage()

        
    def create(self, cls: type, args: tuple):
        self.object_id += 1
        self.objects[self.object_id] = cls(self.object_id, *args)
    
    def destroy(self, id):
        del self.objects[id]

    def setup(self):
        self.create(Player, (60, 60, 32, 32, DisplayManager.get_rectangle_image(32, 32, (0,0,0,100))))
        self.dm.refresh(self.objects.values())
        pass
    

    def manage(self):
        while True:
            if self.fps_alarm.resetAlarm():
                self.dm.refresh(self.objects.values())
            


class UserInfo:

    filename1 = 'playerInfo.sav'
    filename2 = 'playerDat.sav'

    def __init__(self):
        self.gold = 0
        self.score = 0
        self.high_score = 0
        self.play_time = 0              # int
        self.init_time = time.time()    # float
        
        self.inventory = dict()     # key: str (item's name), value: int (quantity)
        self.item_set = dict()      # key: str (item's place), value: str (item's name)

    def load_file(self):

        with open(UserInfo.filename1, 'r') as f:
            vals = f.readline()
            if vals is not line: return

            vals = vals.split(', ')
            self.gold = int(vals[0])
            self.score = int(vals[1])
            self.high_score = int(vals[2])
            self.play_time = int(vals[3])
        
        # save inventory data
        with open(UserInfo.filename2, 'r') as f:
            if f.readline() is not line: return

            r = csv.reader(f)
            self.inventory = dict(zip(r[0], r[1]))
            
        print('load complete')
    

    def save_file(self):

        self.play_time += int(time.time() - self.init_time)
        with open(UserInfo.filename1, 'w') as f:
            f.write(self.to_csv_format)
        
        with open(UserInfo.filename2, 'w') as f:
            w = csv.writer(f)
            w.writerow(self.inventory.keys())
            w.writerow(self.inventory.values())

        print('save complete.')
            
    
    # gold, score, high_score, play_time
    def to_csv_format(self):
        return f'{gold}, {score}, {high_score}, {play_time}'
    
    def playtime_to_string(self):
        tmp = self.play_time

        SEC_IN_DAY = 60*60*24
        SEC_IN_HOUR = 3600
        SEC_IN_MIN = 60

        d = tmp // SEC_IN_DAY * SEC_IN_DAY
        tmp -= d
        h = tmp // SEC_IN_HOUR * SEC_IN_HOUR
        tmp -= h
        m = tmp // SEC_IN_MIN * SEC_IN_MIN
        tmp -= m
        s = tmp

        return f'{d//SEC_IN_DAY}days, {h//SEC_IN_HOUR}hours {m//SEC_IN_MIN}minutes {s}seconds'
        
        

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
        


# All Characters (Player, Enemy) must be extended by this class
class Character(GameObject):

    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)

    def move(self, x, y):
        self.center.move(x, y)
        
    def move_to(self, x, y):
        self.center.move_to(x, y)



class Enemy(Character):
    
    def __init__(self, id, x, y, width, height, image=None):
        super.__init__(id, x, y, width, height, image)
        self.drop_rate = 0.3    # or else

    def __del__(self):
        # motion for destructing
        import random as r
        if r.random() < self.drop_rate:
            pass # generate gold, item, or else

    def move(self, x, y):
        self.center.move(x, y)
        
    def move_to(self, x, y):
        self.center.move_to(x, y)

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



class Controller:
    def __init__(self):

        print('Controller init...', end=' ')

        '''
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000
        '''
        self.input_dict = dict()
        self.unactivated_keys = dict()

        # Input pins:
        self.input_dict['A'] = DigitalInOut(board.D5)
        self.input_dict['A'].direction = Direction.INPUT

        self.input_dict['B'] = DigitalInOut(board.D6)
        self.input_dict['B'].direction = Direction.INPUT

        self.input_dict['L'] = DigitalInOut(board.D27)
        self.input_dict['L'].direction = Direction.INPUT

        self.input_dict['R'] = DigitalInOut(board.D23)
        self.input_dict['R'].direction = Direction.INPUT

        self.input_dict['U'] = DigitalInOut(board.D17)
        self.input_dict['U'].direction = Direction.INPUT

        self.input_dict['D'] = DigitalInOut(board.D22)
        self.input_dict['D'].direction = Direction.INPUT

        '''
        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT
        '''
        print('Complete')

    def is_pressed(self, key: str) -> bool:
        return (not self.input_dict[key])
    
    def get_input(self) -> dict:
        res = dict()
        for key, value in self.input_dict.items():
            res[key] = not value;
        
        return res
    
    # return dict, which only has input values as True
    def get_valid_input(self) -> dict:
        res = dict()
        for key, value in self.input_dict.items():
            if not value: res[key] = not value;
        
        return res
    
    def unactivate(self, key: str):
        self.unactivated_keys[key] = self.input_dict[key]   # backup for re-activate
        self.input_dict[key] = True                         # always no signal
    
    def activate(self, key: str):
        self.input_dict[key] = self.unactivated_keys[key]   # re-activate
        del self.unactivated_keys[key]                      # and then remove from unactivated-list
