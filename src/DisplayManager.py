from digitalio import DigitalInOut
from adafruit_rgb_display import st7789
from PIL import Image, ImageDraw, ImageFont
import board

class DisplayManager:

    bg_length = 240

    def __init__(self):
        
        self.width = DisplayManager.bg_length
        self.height = DisplayManager.bg_length

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

    def refresh(self):
        pass
    
    def set_background(self, fill: tuple):
        bg = ImageDraw.Draw(Image.new("RGB", (self.width, self.height)))

    def display(self, image):
        self.disp.image(image) #todo

def main():
    dp = DisplayManager()
    # paper
    my_image = Image.new("RGBA", (dp.width, dp.height))
    # pen (on the paper)
    my_draw = ImageDraw.Draw(my_image)
    # with pen, draw a rectangle (on the paper)
    my_draw.rectangle((0, 0, dp.width, dp.height), fill=(255, 0, 0, 100))
    # disp shows paper
    dp.display(my_image)
    
    import time
    time.sleep(10)
    my_draw.rectangle((0, 0, dp.width, dp.height), fill = (255, 255, 255, 100))
    dp.display(my_image)

if __name__ == '__main__': main()