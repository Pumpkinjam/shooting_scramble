from pkjgame import *

from digitalio import DigitalInOut
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont
import board

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

        #self.refresh()
        
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
        ImageDraw.Draw(self.bg).rectangle((0, 0, self.width, self.height), fill)    # bg becomes new background
        self.refresh(self.objects)  # update!
    
    # if img not None, set instance(DisplayManager)'s paper to img
    def display(self, room=None):
        if room is not None: self.paper = room.get_image()
        self.disp.image(self.paper)

    def paste_something(self, img: Image, position: tuple) -> None:
        self.paper.paste(img, position)
        self.display()
    
    @staticmethod
    def image_build(img_width, img_height, background=None, obj_list=None) -> Image:
        if background is None:
            background = Image.new("RGBA", (img_width, img_height))
        
        paper = background
        
        for obj in obj_list:
            if not isinstance(obj, GameObject):
                print('DisplayManager.image_build() : given objects must be GameObject')
            else:
                paper.paste(obj.img, obj.center.to_tuple())
        
        return paper

    @staticmethod
    def get_rectangle_image(width: int, height: int, color: tuple):
        rec = Image.new('RGBA', (width, height))
        ImageDraw.Draw(rec).rectangle((0, 0, 32, 32), fill=color)
        return rec