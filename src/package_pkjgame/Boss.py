class Boss(Character):
    
    def __init__(self, room, id, x, y, width=30, height=120, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.speed = 1
        self.hp = HP(20)
        self.am = AlarmManager()
        self.chase_alarm = self.am.new_alarm(1)
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/res/spr_Boss.png", 'rb')))

        self.hpbar = None

    def act(self, input_devices: tuple):
        super().act(input_devices)
        
        if self.hpbar is None: self.hpbar = self.room.create_object(HPBar, (self.hp, self.x + int(self.width * 0.1), self.y - 20, int(self.width * 0.8), 8, None, self))

        if self.chase_alarm.isDone(unactivate=False): 
            #for but in input_devices[0].get_valid_input:
            #   if but in ('A', 'B'): continue
            player_pos = self.room.obj_player.center

            if player_pos.is_above_than(self.center):
                self.move_by_dir(self.speed, SimpleDirection.UP)
            elif player_pos.is_below_than(self.center):
                self.move_by_dir(self.speed, SimpleDirection.DOWN)
            else: self.chase_alarm.resetAlarm()
        
        ''' ## Boss is no longer enemy!
        if self.fire_alarm.resetAlarm():
            self.room.create_object(Laser, (self.center_x, self.room.obj_player.center_y, 8, 2, None, 3, SimpleDirection.RIGHT))
        '''

        if self.center.distance_to(self.room.obj_player.center) < 16:
            # something more...?
            print('oops')
            self.room.obj_player.destroy()

        if self.hp.is_zero():
            print('boss destroyed')
            self.destroy()
            self.room.obj_player.destroy()

    def on_hit(self, dmg=1):
        self.hp.damage(dmg)

class HP:
    
    def __init__(self, max_hp, current_hp=None):
        self.max_hp = max_hp
        self.current_hp = max_hp if current_hp is None else current_hp
    
    def is_zero(self):
        return self.current_hp <= 0
    
    def damage(self, deal):
        self.current_hp -= deal

    def heal(self, heal):
        self.current_hp += heal
        if self.current_hp > self.max_hp: self.current_hp = self.max_hp

    
class HPBar(GameObject):
    
    def __init__(self, room, id, hp, x=0, y=0, width=240, height=8, image=None, relative_instance:GameObject =None):
        super().__init__(room, id, x, y, width, height, image)
        self.hp = hp
        self.relative_instance = relative_instance
        if relative_instance is not None:
            self.relative_x = relative_instance.x - self.x
            self.relative_y = relative_instance.y - self.y
        
        self.refresh()

    def act(self, _):
        self.refresh()
        if self.relative_instance is not None:
            self.move_to(self.relative_instance.x - self.relative_x, self.relative_instance.y - self.relative_y)
    
    def refresh(self):
        hp_ratio = self.hp.current_hp/self.hp.max_hp
        self.img = DisplayManager.get_rectangle_image(self.width, self.height, (0,255,0,255))
        ImageDraw.Draw(self.img).rectangle((0, 0, self.width*hp_ratio, self.height), fill=(255,0,0,255))