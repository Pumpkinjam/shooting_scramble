class Player(Character):
    
    weapon_list = []    # to be implemented (here, or maybe in other class)
    shield_list = []
    state_list = []
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.head(SimpleDirection.RIGHT)
        self.speed = 2

        self.am = AlarmManager()
        
        self.magazine_capacity = 20
        self.magazine_remain = 20
        self.shoot_delay = 0.2
        self.reload_delay = 2
        self.shoot_alarm = self.am.new_alarm(self.shoot_delay)
        self.reload_alarm = self.am.new_alarm(0.01)
        #self.state
        #self.hp

    def __del__(self):
        raise GameManager.GameEndException('Game Over.')

    def act(self, input_devices):
        if self.reload_alarm.isDone():
            self.magazine_remain = self.magazine_capacity
        
        for dev in input_devices:
            if type(dev) == Controller:
                self.command(dev.get_valid_input())
    
    def on_hit(self, dmg=1):
        # todo: on hit actions
        self.move(-dmg, 0)
        pass

    def reload(self):
        if self.reload_alarm.unactivated:
            print('reloading...')
            self.reload_alarm.setClock(self.reload_delay)

    # if holding gun-type weapon... launch_projectile()
    # else... something
    def attack(self, dir):
        #print(self.reload_alarm.clock)
        #print(self.shoot_alarm.clock)
        if self.magazine_remain > 0:
            if self.reload_alarm.unactivated and self.shoot_alarm.resetAlarm():
                self.magazine_remain -= 1
                self.launch_projectile(dir)
            elif not self.reload_alarm.unactivated:
                print('cannot shoot : current reloading.')
        else:
            self.reload()
        

    def launch_projectile(self, dir):
        i = self.room.create_object(Bullet, (self.center_x-4, self.center_y-4, 8, 8, None, 10, dir))

    ''' !! this manual is old-version
    A : weapon -> attack, shield -> defense
    B : pause  (not be processed here)
    U : head the weapon/shield upside, while pushing
    D : swap the weapon/shield
    L : head the weapon/shield leftside, while pushing
    R : skill
    '''

    def head(self, dir: SimpleDirection):
        file_path = abspath(os.getcwd()) + r"/res/spr_Player_{}.png"
        file_name_dir = {
            SimpleDirection.UP : 'up',
            SimpleDirection.LEFT : 'left',
            SimpleDirection.RIGHT : 'right',
            SimpleDirection.DOWN : 'down'
        }

        self.set_img(Image.open(open(file_path.format(file_name_dir[dir]), 'rb')))
        self.heading = dir



    def command(self, input_sig: tuple):
        # default direction is right side.
        if ('U' not in input_sig) and ('L' not in input_sig) and ('D' not in input_sig):
            self.head(SimpleDirection.RIGHT)

        for cmd in input_sig:
            if cmd == 'A':
                self.attack(self.heading)
            elif cmd == 'U':
                #self.head(SimpleDirection.UP)
                self.move_by_dir(self.speed, SimpleDirection.UP)
            elif cmd == 'L':
                self.reload()
            elif cmd == 'D':
                self.move_by_dir(self.speed, SimpleDirection.DOWN)
                pass
            elif cmd == 'R':
                pass