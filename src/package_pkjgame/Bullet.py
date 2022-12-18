class Bullet(GameObject):
    def __init__(self, room, id, x, y, width, height, image=None, speed=1, dir=SimpleDirection.RIGHT):
        super().__init__(room, id, x, y, width, height, image)
        self.speed = speed
        self.dir = dir
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/res/spr_Bullet.png", 'rb')))
    
    '''
    def __del__(self):
        pass # add some effects?
    '''
    
    def act(self, input_devices:tuple):
        self.move_by_dir(self.speed, self.dir)

        if (not self.is_in_room()):
            self.destroy()

        # wait, what...?
        for targ in list(self.room.objects.values()):
            
            if self.check_collision(targ):
                if isinstance(targ, Enemy):
                    print("Bullet hit!!")
                    targ.destroy(on_hit=True)
                    self.destroy()
                elif type(targ) == Laser and not targ.reflected:
                    targ.reflect()


class Laser(GameObject):
    def __init__(self, room, id, x, y, width, height, image=None, speed=1, dir=SimpleDirection.RIGHT):
        super().__init__(room, id, x, y, width, height, image)
        self.speed = speed
        self.dir = dir
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/res/spr_Laser.png", 'rb')))
        self.reflected = False
    
    def act(self, input_devices:tuple):
        self.move_by_dir(self.speed, self.dir)

        if (not self.is_in_room()):
            self.destroy()

        if self.check_collision(self.room.obj_player):
            print("Laser hit!!")
            self.room.obj_player.on_hit()
            self.destroy()
        elif self.check_collision(self.room.obj_boss):
            print("Boss : laser hit!")
            self.room.obj_boss.on_hit(1)
            self.destroy()

    def reflect(self):
        self.reflected = True
        if random.random() < 0.5:
            self.dir = SimpleDirection.RUP
        else:
            self.dir = SimpleDirection.RDOWN