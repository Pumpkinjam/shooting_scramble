class Enemy(Character):
    
    def __init__(self, room, id, x, y, width=16, height=16, image=None, dir=SimpleDirection.LEFT):
        super().__init__(room, id, x, y, width, height, image)
        #self.speed = self.room.speed
        self.dir = dir
        self.drop_rate = 0.9    # or else

    def __del__(self):
        # todo: motion for destructing
        if self.is_dropped():
            print('drop!')
            self.room.create_object(Gold, (self.center_x - Gold.size//2, self.center_y - Gold.size//2, None, self.dir))
            pass # generate gold, item, or else
            
    def destroy(self):
        self.room.del_object(self)
    
    def act(self, input_devices: tuple):
        self.move_by_dir(self.room.speed, self.dir)

        #print(self, self.center.is_left_than(Pos(0,0)))
        if self.center.is_left_than(Pos(0, 0)):
            self.destroy()

        if self.check_collision(self.room.obj_player):
            self.room.obj_player.on_hit(3)
            self.destroy()

    def is_dropped(self):
        return random.random() < self.drop_rate


class Boss(Character):
    
    def __init__(self, room, id, x, y, width=30, height=120, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.am = AlarmManager()
        self.fire_alarm = self.am.new_alarm(5)
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/../res/spr_Boss.png", 'rb')))

    def act(self, _: tuple):
        # todo : randomize the delay
        if self.fire_alarm.resetAlarm():
            self.room.create_object(Laser, (self.center_x, self.room.obj_player.center_y, 8, 2, None, 3, SimpleDirection.RIGHT))

        if self.check_collision(self.room.obj_player):
            # something more...?
            print('oops')
            self.room.obj_player.destroy()
