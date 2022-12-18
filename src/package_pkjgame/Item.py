class Item(GameObject):
    size = 8
    def __init__(self, room, id, x, y, image=None, dir=None):
        # actually, speed and dir must not be None
        super().__init__(room, id, x, y, Item.size, Item.size, image)
        self.dir = dir
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/res/spr_item.png", 'rb')))

    def act(self, _):
        self.move_by_dir(self.room.speed, self.dir)

        if self.center.is_left_than(Pos(0, 0)):
            self.destroy()
        
        if self.check_collision(self.room.obj_player):
            self.gain_effect()

    def gain_effect(self):
        print(f"item get")
        
        tmp = random.random()
        
        if (tmp < 0.2):     # 20% - player movement to right
            print('player acceleration')
            for i in range(3):
                self.room.obj_player.move_by_dir(1, SimpleDirection.RIGHT)
        elif tmp < 0.4:     # 20% - boss heal by half-hp
            print('boss heal')
            self.room.obj_boss.hp.heal(self.room.obj_boss.hp.max_hp // 2)
        elif tmp < 0.6:     # 20% - remove all laser
            print('bomb')
            for obj in list(self.room.objects.values()):
                if isinstance(obj, Laser):
                    self.room.del_object(obj)
        elif tmp < 0.8:     # 20% - launch bullets to all directions
            print('bullet storm')
            for dir in SimpleDirection:
                self.room.obj_player.launch_projectile(dir)
        else:               # that's unlucky
            print('lose...')

        self.destroy()


class Gold(Item):
    def __init__(self, room, id, x, y, image=None, dir=None):
        # actually, speed and dir must not be None
        super().__init__(room, id, x, y, image, dir)
        self.set_img(Image.open(open(abspath(os.getcwd()) + r"/res/spr_coin.png", 'rb')))

    def gain_effect(self):
        print(f"gold++; current : {self.room.user_info.gold}")
        self.room.user_info.gold += 1
        self.destroy()