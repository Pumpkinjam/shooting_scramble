import time
import random
from abc import *
import numpy as np
from math import sqrt
import csv

from PIL import Image, ImageDraw, ImageFont
import copy
import board
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789


#############################################################################
#                                                                           #
# GameManager.py                                                            #
#                                                                           #
#############################################################################


class GameManager:
    
    def __init__(self, fps, screen_width, screen_height):
        self.fps = fps
        self.spf = 1/fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.object_id = 0


    def start(self):
        self.setup()
        self.manage()
        '''
        try:
            self.manage()
        except:
            print('what')
            return
            '''

    def stop(self):
        raise GameManager.GameEndException('Game Stopped.')

    def setup(self):
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.rm = RoomManager(self.screen_width, self.screen_height)
        self.user = UserInfo()
        
        self.rm.create_room(self.screen_width, self.screen_height)
        self.player = self.create(Player, (60, 60, 32, 32, DisplayManager.get_rectangle_image(32, 32, (0,0,0,100))))

        self.fps_alarm = self.am.new_alarm(self.spf)
        
        self.disp()

    def manage(self):
        i=0
        while True:
            i+=1
            self.player.move(1 if i//50%2==0 else -1, 0)
            #self.create(Player, (self.player.x, self.player.y, 32, 32, DisplayManager.get_rectangle_image(32, 32, (random.randint(0,255), random.randint(0,255), random.randint(0,255), 100))))
            if self.fps_alarm.resetAlarm():
                self.disp()
                print(self.player.x, self.player.y)
                print(self.fps_alarm.clock)
                print(f'current number of object : {len(self.rm.current_room.objects)}')


    def create(self, cls: type, args: tuple):
        return self.rm.current_room.create_object(cls, args)
    
    def destroy(self, id) -> None:
        del self.objects[id]

    def disp(self) -> None:
        self.dm.display(self.rm.current_room)


    class GameEndException(Exception):
        def __init__(self, msg=''):
            print('Game Ended' if msg == '' else msg)
            super().__init__(msg)


#############################################################################
#                                                                           #
# Pos.py                                                                    #
#                                                                           #
#############################################################################


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
        return sqrt((self.x - other.x) ** 2  + (self.y - other.y) ** 2)
    
    def to_tuple(self) -> tuple:
        return (self.x, self.y)
    
    def to_string(self) -> str:
        return f'[Pos ({self.x}, {self.y})]'


#############################################################################
#                                                                           #
# AlarmManager.py                                                           #
#                                                                           #
#############################################################################

class Alarm:
    '''
    float clock; // once Alarm have been done, clock becomes -1
    float start_time;
    float timing;

    int id;
    '''
    def __init__(self, id, set_time):
        self.id = id
        self.set_time = set_time   # fixed
        self.clock = set_time      # reduces
        self.unactivated = False
        self.start_time = time.time()
        self.timing = self.start_time + self.clock
    
    # return if the valid alarm was done
    def isDone(self) -> bool:
        #print(self.unactivated)
        if self.unactivated: return False
        self.clock = self.timing - time.time()

        if (self.clock <= 0):
            #print('Alarm Done!')
            self.unactivated = True
            return True
        else:
            #print('wait...')
            return False
    

    def getPassedTime(self) -> float:
        if self.unactivated: return -1.

        tmp = self.timing - time.time()
        if tmp < 0: return -1.
        else: return tmp
        
    '''
    # reset the start_time and clock (with new_clock)
    def setClock(self, new_time) -> None:
        self.unactivated = False
        self.start_time = time.time()
        self.set_time = new_time
        self.clock = new_time
        self.timing = self.start_time + self.clock
    '''

    # if alarm is done, set Alarm with new_clock and return True
    # else, return False
    def resetAlarm(self, new_time=None) -> bool:
        #print(f'Alarm clock check : {self.clock}')
        if not self.isDone(): return False

        self.started_time = time.time()
        if new_time is not None:
            self.set_time = new_time
            self.clock = new_time
            self.timing = self.started_time + self.new_time
        else:
            self.clock = self.set_time
            self.timing = self.started_time + self.set_time
        
        self.unactivated = False
        return True


class AlarmManager:

    def __init__(self):
        self.current_id = 0  # primary key for alarms
        self.alarms = dict()
        # self.threads = dict()
    
    def new(self, t=-1): return self.new_alarm(t)
    def new_alarm(self, t=-1) -> Alarm:
        self.current_id += 1
        return self._new_alarm(self.current_id, t)

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



#############################################################################
#                                                                           #
# DisplayManager.py                                                         #
#                                                                           #
#############################################################################


class DisplayManager:
    
    bg_length = 240

    def __init__(self):
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

        self.display()
        
    """
    def refresh(self, obj_list=None):
        self.paper = DisplayManager.image_build(self.width, self.height, self.bg, obj_list)
        '''
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
        
        '''
        self.display()
    """
    
    def set_background(self, fill: tuple):
        ImageDraw.Draw(self.bg).rectangle((0, 0, self.width, self.height), fill=fill)    # bg becomes new background
        self.refresh(self.objects)  # update!
    
    # if img not None, set instance(DisplayManager)'s paper to img
    def display(self, room=None):
        if room is not None: self.paper = room.reset_image()
        self.disp.image(self.paper)

    def paste_something(self, img: Image, position: tuple) -> None:
        self.paper.paste(img, position, img)
        self.display()
    
    @staticmethod
    def image_build(img_width, img_height, background=None, obj_dict=None) -> Image:
        if background is None:
            background = Image.new("RGBA", (img_width, img_height))
        
        paper = background
        
        for obj in obj_dict.values():
            if not isinstance(obj, GameObject):
                print()
                raise Exception('DisplayManager.image_build() : given objects must be GameObject')
            else:
                paper.paste(obj.img, obj.center.to_tuple(), obj.img)
        
        return paper

    @staticmethod
    def get_rectangle_image(width: int, height: int, color: tuple):
        rec = Image.new('RGBA', (width, height))
        ImageDraw.Draw(rec).rectangle((0, 0, 32, 32), fill=color)
        return rec


#############################################################################
#                                                                           #
# RoomManager.py                                                            #
#                                                                           #
#############################################################################


class Room:

    def __init__(self, id, room_width, room_height, bg=None, objs=dict()):
        self.id = id
        self.object_id = 0
        self.width = room_width
        self.height = room_height
        self.objects = objs        # keys: id (int), values: obj (GameObject)
        self.deleted = False
        if bg is None:
            self.background = Image.new("RGBA", (room_width, room_height))
            ImageDraw.Draw(self.background).rectangle((0, 0, room_width, room_height), (255,255,255,100))
        else:
            self.background = bg
        self.image = copy.deepcopy(self.background)

        self.reset_image()

    def reset_image(self):
        self.image = DisplayManager.image_build(self.width, self.height, self.background, self.objects)
        return self.image

    def create_object(self, cls: type, args: tuple):
        self.object_id += 1
        obj = cls(self.object_id, *args)

        self.objects[self.object_id] = obj
        
        print(f'{cls} created.')
        self.reset_image()
        return obj
    
    def del_object(self, obj):
        del self.objects[obj.id]
        self.reset_image()
    
    def get_objects(self):
        return self.objects

    def get_image(self):
        return self.image
    
    
class RoomManager:

    def __init__(self, first_room_width, first_room_height):
        self.current_id = 0
        self.number_rooms = 0
        self.rooms = dict()

        r = self.create_room(first_room_width, first_room_height)
        self.first_room = r
        self.current_room = r

    def create_room(self, room_width, room_height, objs=dict()):
        self.number_rooms += 1
        self.current_id += 1
        r = Room(self.current_id, room_width, room_height, objs=objs)

        if self.number_rooms == 1:
            self.first_room = r
            self.current_room = r

        self.rooms[self.current_id] = r
        return r

    # move to another room before deletion
    # else, RoomManager automatically set current_room to first_room
    def del_room(self, room: Room):
        if room.id not in self.rooms.keys():
            print('from del_room : that room does not belong to this manager.')
            return
        
        self.number_rooms -= 1
        if (self.number_rooms == 0): raise RoomManager.NoRoomException()

        # trying to delete first_room
        if self.first_room == room:
            for r in self.rooms.values():
                if r != room: self.first_room = r
                break
        
        # trying to delete current_room
        if self.current_room == room:
            self.current_room = self.first_room
        
        room.deleted = True
        del self.rooms[room.id]

    def goto_room(self, room=None, room_id=None):
        if (room is None and room_id is None): 
            print('goto_room must have at least 1 arguments.')
            raise Exception()
        
        if room_id is None:
            self.current_room = room
        elif room is None:
            self.current_room = self.rooms[room_id]

    class NoRoomException(Exception):
        def __init__(self, msg=''):
            print('No more rooms in RoomManager.' if msg == '' else msg)
            super().__init__(msg)
        

#############################################################################
#                                                                           #
# UserInfo.py                                                               #
#                                                                           #
#############################################################################


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


#############################################################################
#                                                                           #
# GameObject.py                                                             #
#                                                                           #
#############################################################################


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
            self.img = Image.new("RGBA", (width, height))
        
        self.id = id
        self.state = None
        self.center = Pos(x, y)
        self.x = x
        self.y = y
        self.outline = "#FFFFFF"


    def move(self, x, y):
        self.center.move(x, y)
        self.x = self.center.x
        self.y = self.center.y
        
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


#############################################################################
#                                                                           #
# Character.py                                                              #
#                                                                           #
#############################################################################


# All Characters (Player, Enemy) must be extended by this class
class Character(GameObject):

    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)


#############################################################################
#                                                                           #
# Enemy.py                                                                  #
#                                                                           #
#############################################################################


class Enemy(Character):
    
    def __init__(self, id, x, y, width, height, image=None):
        super.__init__(id, x, y, width, height, image)
        self.drop_rate = 0.3    # or else

    def __del__(self):
        # motion for destructing
        import random as r
        if r.random() < self.drop_rate:
            pass # generate gold, item, or else


#############################################################################
#                                                                           #
# Player.py                                                                 #
#                                                                           #
#############################################################################


class Player(Character):

    weapon_list = []    # to be implemented (here, or maybe in other class)
    shield_list = []
    state_list = []
    
    def __init__(self, id, x, y, width, height, image=None):
        super().__init__(id, x, y, width, height, image)
        #self.state
        #self.hp


#############################################################################
#                                                                           #
# Controller.py                                                             #
#                                                                           #
#############################################################################


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
