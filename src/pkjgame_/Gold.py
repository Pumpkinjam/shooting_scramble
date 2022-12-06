class Gold(GameObject):
    size = 8
    def __init__(self, room, id, x, y, image=None, dir=None):
        # actually, speed and dir must not be None
        super().__init__(room, id, x, y, Gold.size, Gold.size, image)
        self.dir = dir
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/../res/spr_coin.png", 'rb')))
    
    def __del__(self):
        pass
        #print("gold get!")

    def act(self, _):
        self.move_by_dir(self.room.speed, self.dir)

        if self.center.is_left_than(Pos(0, 0)):
            self.destroy()
        
        if self.check_collision(self.room.obj_player):
            print("gold++;") # todo
            self.destroy()
