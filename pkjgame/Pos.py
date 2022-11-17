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