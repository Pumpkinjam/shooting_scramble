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
        self.paper = copy.deepcopy(self.bg)
        #self.pen = ImageDraw.Draw(self.paper)

        self.display()

    
    def set_background(self, fill: tuple):
        ImageDraw.Draw(self.bg).rectangle((0, 0, self.width, self.height), fill=fill)    # bg becomes new background
        self.refresh(self.objects)  # update!
    
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
        
        paper = copy.deepcopy(background)
        
        for obj in obj_dict.values():
            if not isinstance(obj, GameObject):
                print()
                raise Exception('DisplayManager.image_build() : given objects must be GameObject')
            else:
                paper.paste(obj.img, (int(obj.x), int(obj.y)), obj.img)
        
        return paper

    @staticmethod
    def get_rectangle_image(width: int, height: int, color: tuple = (0,0,0,255)):
        rec = Image.new('RGBA', (width, height))
        ImageDraw.Draw(rec).rectangle((0, 0, width, height), fill=color)
        return rec

    @staticmethod
    def get_text_image(width: int, height: int, msg: str, color: tuple = (0,255,0)):
        txt = DisplayManager.get_rectangle_image(width, height, (20,20,20,50))
        ImageDraw.Draw(txt).text((2, 2), msg, color)
        return txt