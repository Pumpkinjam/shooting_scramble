class Bullet(GameObject):
    def __init__(self, room, id, x, y, width, height, image=None, speed=1, dir=SimpleDirection.RIGHT):
        super().__init__(room, id, x, y, width, height, image)
        self.speed = speed
        self.dir = dir
    
    '''
    def __del__(self):
        pass # add some effects?
'''
    def destroy(self):
        self.room.del_object(self)
    
    def act(self, input_devices:tuple):
        if (not self.is_in_room()):
            self.destroy()
        self.move_by_dir(self.speed, self.dir)