# All Characters (Player, Enemy, ...) must be extended by this class
class Character(GameObject):
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.shadow = self.get_range()

    def act(self, input_devices: tuple):
        self.shadow = self.get_range()

    def check_collision(self, other):
        res =  self.is_in_range(other.get_range()) or other.is_in_range(other.get_range()) or other.is_in_range(self.shadow)
        if isinstance(other, Character):
            res = res or self.is_in_range(other.shadow)
        
        return res