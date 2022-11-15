from pkjgame import *

from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789
import board

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
    


    
    