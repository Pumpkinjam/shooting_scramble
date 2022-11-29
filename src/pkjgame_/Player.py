class Player(Character):
    
    weapon_list = []    # to be implemented (here, or maybe in other class)
    shield_list = []
    state_list = []
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.heading = SimpleDirection.RIGHT
        #self.state
        #self.hp

    def __del__(self):
        raise GameManager.GameEndException('Game Over.')

    def act(self, input_devices):
        for dev in input_devices:
            if type(dev) == Controller:
                self.command(dev.get_valid_input())
    
    def on_hit(self):
        # todo: on hit actions (move slightly to left)
        pass

    # if holding gun-type weapon... launch_projectile()
    # else... something
    def attack(self, dir):
        self.launch_projectile(dir)
        pass

    def launch_projectile(self, dir):
        i = self.room.create_object(Bullet, (*(self.center.to_tuple()), 4, 4, DisplayManager.get_rectangle_image(4, 4), 10, dir))

    '''
    A : weapon -> attack, shield -> defense
    B : pause  (not be processed here)
    U : head the weapon/shield upside, while pushing
    D : swap the weapon/shield
    L : head the weapon/shield leftside, while pushing
    R : skill
    '''
    def command(self, input_sig: tuple):
        # default direction is right side.
        print(self.heading)
        
        if ('U' not in input_sig) and ('L' not in input_sig):
            self.heading = SimpleDirection.RIGHT

        for cmd in input_sig:
            if cmd == 'A':
                self.attack(self.heading)
            elif cmd == 'U':
                self.heading = SimpleDirection.UP
            elif cmd == 'L':
                self.heading = SimpleDirection.LEFT
            elif cmd == 'D':
                self.heading = SimpleDirection.DOWN
                pass
            elif cmd == 'R':
                pass