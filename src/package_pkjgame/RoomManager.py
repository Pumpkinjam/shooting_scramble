class Room:
    
    def __init__(self, id, room_width, room_height, user_info, bg=None, objs=dict()):
        self.id = id
        self.object_id = 0
        self.width = room_width
        self.height = room_height
        self.objects = objs        # keys: id (int), values: obj (GameObject)
        self.deleted = False

        self.user_info = user_info

        self.original_bg = bg
        if bg is None:
            self.background = Image.new("RGBA", (room_width, room_height))
            ImageDraw.Draw(self.background).rectangle((0, 0, room_width, room_height), (255,255,255,100))
        else:
            self.set_background(bg)

        self.image = copy.deepcopy(self.background)

        self.am = AlarmManager()
        
        self.obj_player = None  # not None only in the GameRoom
        self.obj_boss = None    # too

        self.reset_image()

    # make objects in room do something specific actions
    def objects_act(self, input_devices: tuple):
        for obj in list(self.objects.values()):
            obj.act(input_devices)
        
    def reset_image(self):
        self.image = DisplayManager.image_build(self.width, self.height, self.background, self.objects)
        return self.image

    # makes object with room, id
    def create_object(self, cls: type, args: tuple):
        #print(f'creating {cls}')

        self.object_id += 1
        obj = cls(self, self.object_id, *args)

        self.objects[self.object_id] = obj
        
        self.reset_image()

        if cls == Player:
            if self.obj_player is not None:
                raise Exception("the Player already exists!")
            else:
                self.obj_player = obj

        if cls == Boss:
            if self.obj_boss is not None:
                raise Exception("the Boss already exists!")
            else:
                self.obj_boss = obj

        return obj
    
    def del_object(self, obj):
        if obj == self.obj_player:
            raise GameManager.GameEndException('Game over.')
        
        try:
            del self.objects[obj.id]
        except:
            print(f'KeyError : {obj.id}')
            for k, v in self.objects.items():
                print(k, v)
        
        gc.collect()
        self.reset_image()
    
    def get_objects(self):
        return self.objects

    def get_image(self):
        return self.image

    def set_background(self, new_bg=None, offset=(0,0)):
        if new_bg is not None: self.original_bg = new_bg

        left = offset[0]
        upper = offset[1]
        right = left+240
        bottom = upper+240
        self.background = self.original_bg.crop((left, upper, right, bottom))
        
    

class GameRoom(Room):
    def __init__(self, id, room_width, room_height, user_info, bg=None, objs=dict()):
        super().__init__(id, room_width, room_height, user_info, bg, objs)

        self.enemy_spawn_delay = 5
        self.speed = 3
        self.enemy_spawn_alarm = self.am.new_alarm(self.enemy_spawn_delay)

        self.bg_offset = 0
        self.set_background(Image.open(open(abspath(os.getcwd()) + r"/res/background/bg_game_blended.png", 'rb')))

        self.room_speed_alarm = self.am.new_alarm(5)
    
    
    def objects_act(self, input_devices):
        super().objects_act(input_devices)

        self.bg_offset = (self.bg_offset + self.speed//2) % 960
        self.set_background(offset=(self.bg_offset, 0))
        
        if self.room_speed_alarm.resetAlarm():
            self.speed += 0.5
        
        if self.enemy_spawn_alarm.resetAlarm(2 if self.speed > 10 else (5 - self.speed * 3 / 10)):
            self.spawn_enemy()
            #print(f'number of objects in this room : {len(self.objects)}')
    
    def spawn_enemy(self):
        enemy_img = Image.open(open(abspath(os.getcwd()) + r"/res/spr_Mob_from_right.png", 'rb'))
        enemy_speed = self.speed*1.2

        tmp = random.random()

        if tmp < 0.4:
            instance_class = Firing_Enemy
            enemy_speed = 4

            if tmp < 0.15:      # down -> up
                spawn_x = 180
                spawn_y = 240
                move_dir = SimpleDirection.UP

            elif tmp < 0.3:     # up -> down
                spawn_x = 180
                spawn_y = -16
                move_dir = SimpleDirection.DOWN

            elif tmp < 0.35:    # -> ldwon
                spawn_x = 240
                spawn_y = 0
                enemy_speed = 3
                move_dir = SimpleDirection.LDOWN

            else:               # -> lup
                spawn_x = 240
                spawn_y = 240
                enemy_speed = 3
                move_dir = SimpleDirection.LUP

        else:                   # right -> left
            instance_class = Enemy
            spawn_x = 240
            spawn_y = (self.obj_player.center_y + self.obj_player.y) // 2 + random.randint(-5, 5)
            move_dir = SimpleDirection.LEFT

            if tmp > 0.95:      # in-formation
                enemy_speed //= 4
                self.create_object(instance_class, (spawn_x-16, spawn_y-20, 16, 16, enemy_speed//4, enemy_img, move_dir))
                self.create_object(instance_class, (spawn_x+16, spawn_y+20, 16, 16, enemy_speed//4, enemy_img, move_dir))

        self.create_object(instance_class, (spawn_x, spawn_y, 16, 16, enemy_speed, enemy_img, move_dir))

    def set_enemy_spawn_delay(self, new_delay: int):
        self.enemy_spawn_delay = new_delay
        self.enemy_spawn_alarm.setClock(new_delay)
        
    
class RoomManager:

    def __init__(self, first_room_width, first_room_height):
        self.current_id = 0
        self.number_rooms = 0
        self.rooms = dict()

        '''
        r = self.create_room(first_room_width, first_room_height)
        self.first_room = r
        self.current_room = r
        '''

    def create_room(self, room_width, room_height, user_info, objs=dict(), game=False):
        self.number_rooms += 1
        self.current_id += 1

        if game:
            roomtype = GameRoom
        else: 
            roomtype = Room
        
        r = roomtype(self.current_id, room_width, room_height, user_info, objs=objs)

        if self.number_rooms == 1:
            self.first_room = r
            self.current_room = r

        self.rooms[self.current_id] = r
        return r

    # move to another room before deletion
    # else, RoomManager automatically set current_room to first_room
    def del_room(self, room: Room):
        if room.id not in self.rooms.keys():
            print('from del_room : that room does not belong to this manager.')
            return
        
        self.number_rooms -= 1
        if (self.number_rooms == 0): raise RoomManager.NoRoomException()

        # trying to delete first_room
        if self.first_room == room:
            for r in self.rooms.values():
                if r != room: self.first_room = r
                break
        
        # trying to delete current_room
        if self.current_room == room:
            self.current_room = self.first_room
        
        room.deleted = True
        del self.rooms[room.id]

    def goto_room(self, room=None, room_id=None):
        if (room is None and room_id is None): 
            raise RoomManager.NoRoomException('goto_room must have at least 1 arguments.')
        
        if room_id is None:
            self.current_room = room
        elif room is None:
            self.current_room = self.rooms[room_id]

    class NoRoomException(Exception):
        def __init__(self, msg=''):
            print('No more rooms in RoomManager.' if msg == '' else msg)
            super().__init__(msg)