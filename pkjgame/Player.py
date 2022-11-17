class Player(Character):
    
    weapon_list = []    # to be implemented (here, or maybe in other class)
    shield_list = []
    state_list = []
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super().__init__(room, id, x, y, width, height, image)
        self.heading = SimpleDirection.RIGHT
        #self.state
        #self.hp

    def act(self, input_devices):
        for dev in input_devices:
            if type(dev) == Controller:
                self.command(dev.get_valid_input())
    

    # if holding gun-type weapon... launch_projectile()
    # else... something
    def attack(self):
        self.launch_projectile()
        pass

    def launch_projectile(self):
        self.room.create_object(Bullet, (*(self.center.to_tuple()), 4, 4, DisplayManager.get_rectangle_image(4, 4), 10, self.heading))


    '''
    A : weapon -> attack, shield -> defense
    B : pause  (not be processed here)
    U : head the weapon/shield upside, while pushing
    D : swap the weapon/shield
    L : head the weapon/shield leftside, while pushing
    R : skill
    '''
    def command(self, input_sig: tuple):
        for cmd in input_sig:
            if cmd == 'A':
                self.attack()
            elif cmd == 'U':
                self.move(0, -1)
                self.heading = SimpleDirection.UP
            elif cmd == 'L':
                self.move(-1, 0)
                self.heading = SimpleDirection.LEFT
            elif cmd == 'D':
                self.move(0, 1)
                self.heading = SimpleDirection.DOWN
                pass
            elif cmd == 'R':
                self.heading = SimpleDirection.RIGHT
                pass
        