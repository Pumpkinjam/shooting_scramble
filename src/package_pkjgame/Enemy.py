class Enemy(Character):
    
    def __init__(self, room, id, x, y, width=16, height=16, speed=1, image=None, dir=SimpleDirection.LEFT):
        super().__init__(room, id, x, y, width, height, image)
        #self.speed = self.room.speed
        self.dir = dir
        self.speed = speed
        self.item_rate = 0.9    # item first. gold drops only when item was not dropped.
        self.drop_rate = 0.2    # or else

    def __del__(self):
        # todo: motion for destructing
        pass
            
    def destroy(self, on_hit=False):
        if on_hit:
            self.room.user_info.score += 5
            if random.random() < self.item_rate:
                print('item!')
                self.room.create_object(Item, (self.center_x - Item.size//2, self.center_y - Item.size//2, None, SimpleDirection.LEFT))

            elif random.random() < self.drop_rate:
                print('drop!')
                self.room.create_object(Gold, (self.center_x - Item.size//2, self.center_y - Item.size//2, None, SimpleDirection.LEFT))
        
        super().destroy()

    def act(self, input_devices: tuple):
        super().act(input_devices)
        self.move_by_dir(self.speed, self.dir)

        if self.center.is_left_than(Pos(0, 0)) or\
        (self.dir == SimpleDirection.UP or self.dir == SimpleDirection.LUP) and self.center.is_above_than(Pos(0,0)) or\
        (self.dir == SimpleDirection.DOWN or self.dir == SimpleDirection.LDOWN) and self.center.is_below_than(Pos(0,240)):
            self.destroy()

        if self.check_collision(self.room.obj_player):
            self.room.obj_player.on_hit(3)
            self.destroy()

        if self.check_collision(self.room.obj_boss):
            self.room.obj_boss.on_hit(5)
            self.destroy()


# move up-downward, fire the laser
class Firing_Enemy(Enemy):
    
    def __init__(self, room, id, x, y, width=16, height=16, speed=1, image=None, dir=SimpleDirection.DOWN, firing_delay=1):
        super().__init__(room, id, x, y, width, height, speed, image, dir)
        self.firing_delay = firing_delay
        self.am = AlarmManager()
        self.fire_alarm = self.am.new_alarm(firing_delay)

    def act(self, _):
        super().act(_)
        if self.fire_alarm.resetAlarm():
            self.room.create_object(Laser, (self.center_x, self.center_y, 8, 2, None, 3, SimpleDirection.LEFT))