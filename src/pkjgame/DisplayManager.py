from pkjgame import *

from digitalio import DigitalInOut
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont
import board

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
            if obj is not GameObject:
                print('Something went wrong...')
            else:
                self.paper = Image.alpha_composite(self.paper, obj.img)
        
          #self.pen = ImageDraw.Draw(self.paper)
        self.display()
    
    def set_background(self, fill: tuple):
        ImageDraw.Draw(self.bg).rectangle((0, 0, self.width, self.height), fill)    # bg becomes new background
        self.refresh(self.objects)  # update!
    
    def display(self):
        self.disp.image(self.paper)
