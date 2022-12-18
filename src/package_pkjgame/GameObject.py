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
    # x, y comes for image (value of lt)
    # in fact, Gameobject's x, y field becomes x+width//2, y+width//2
    def __init__(self, room, id, x, y, width, height, image=None):
        if image is not None:
            self.img = image
        else:
            self.img = Image.new("RGBA", (width, height))

        self.original_img = self.img
        self.visiblity = True
        
        self.room = room
        self.id = id
        self.state = None

        self.center_x = x+width//2
        self.center_y = y+height//2
        self.center = Pos(self.center_x, self.center_y)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.outline = "#FFFFFF"

    def __del__(self):
        pass
        #print(f'{self}[{self.id}] destroyed.')

    @abstractmethod
    def act(self, input_devices: tuple):
        pass
    
    def destroy(self):
        self.room.del_object(self)

    # if dir is not None, arguments x and y will be ignored
    def move(self, x=0, y=0):
        self.center.move(x, y)
        self.x += x
        self.y += y
        self.center_x += x
        self.center_y += y

    def move_by_dir(self, speed, dir):
        if dir == SimpleDirection.RIGHT:
            self.move(speed, 0)
        elif dir == SimpleDirection.LEFT:
            self.move(-speed, 0)
        elif dir == SimpleDirection.UP:
            self.move(0, -speed)
        elif dir == SimpleDirection.DOWN:
            self.move(0, speed)
        elif dir == SimpleDirection.RDOWN:
            self.move(speed, speed)
        elif dir == SimpleDirection.RUP:
            self.move(speed, -speed)
        elif dir == SimpleDirection.LDOWN:
            self.move(-speed, speed)
        elif dir == SimpleDirection.LUP:
            self.move(-speed, -speed)
        else:
            raise Exception('Unknown SimpleDirection')
        
    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.center_x = self.x + self.width//2
        self.center_y = self.y + self.height//2
        self.center = Pos(self.center_x, self.center_y)
        
    def set_visiblity(self, visiblity: bool):
        self.visiblity = visiblity
    
    def get_range(self) -> tuple:   # (Pos1, Pos2)
        return (
            Pos(self.x, self.y), 
            Pos(self.x + self.width, self.y + self.height)
            )
    
    def is_in_range(self, ran: tuple):
        lt = ran[0]; rb = ran[1]
        return (lt.x < self.x < rb.x) and (lt.y < self.y < rb.y)

    def is_in_room(self):
        return self.is_in_range(
            (Pos(0,0), Pos(self.room.width, self.room.height))
            )

    def check_collision(self, other):
        return self.is_in_range(other.get_range()) or other.is_in_range(self.get_range())
    
    def set_img(self, img):
        self.img = img