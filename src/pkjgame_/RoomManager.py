class Room:
    
    def __init__(self, id, room_width, room_height, bg=None, objs=dict()):
        self.id = id
        self.object_id = 0
        self.width = room_width
        self.height = room_height
        self.objects = objs        # keys: id (int), values: obj (GameObject)
        self.deleted = False
        if bg is None:
            self.background = Image.new("RGBA", (room_width, room_height))
            ImageDraw.Draw(self.background).rectangle((0, 0, room_width, room_height), (255,255,255,100))
        else:
            self.background = bg
        self.image = copy.deepcopy(self.background)

        self.am = AlarmManager()
        
        self.obj_player = None  # not None only in the GameRoom

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

        self.object_id += 1
        obj = cls(self, self.object_id, *args)

        self.objects[self.object_id] = obj
        
        #print(f'{cls} created.')
        self.reset_image()

        if cls == Player:
            if self.obj_player is not None:
                raise Exception("the Player already exists!")
            else:
                self.obj_player = obj

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
    

class GameRoom(Room):
    def __init__(self, id, room_width, room_height, bg=None, objs=dict()):
        super().__init__(id, room_width, room_height, bg, objs)

        self.enemy_spawn_delay = 3
        self.speed = 3
        self.enemy_spawn_alarm = self.am.new_alarm(self.enemy_spawn_delay)

        self.room_speed_alarm = self.am.new_alarm(5)
    
    
    def objects_act(self, input_devices):
        super().objects_act(input_devices)
        
        if self.room_speed_alarm.resetAlarm():
            self.speed += 0.5
        
        if self.enemy_spawn_alarm.resetAlarm():
            spawn_x = 240
            spawn_y = 188
            move_dir = SimpleDirection.LEFT
            enemy_img = Image.open(open(r"/home/kau-esw/esw/shooting_scramble/res/spr_Mob_from_right.png", 'rb'))

            if random.random() < 0.4:
                spawn_x = (self.obj_player.center_x + self.obj_player.x)//2
                spawn_y = 0
                move_dir = SimpleDirection.DOWN
                enemy_img = Image.open(open(r"/home/kau-esw/esw/shooting_scramble/res/spr_Mob_from_sky.png", 'rb'))
            
            i = self.create_object(Enemy, (spawn_x, spawn_y, 16, 16, enemy_img, move_dir))
            #print(f'number of objects in this room : {len(self.objects)}')
            

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

    def create_room(self, room_width, room_height, objs=dict(), game=False):
        self.number_rooms += 1
        self.current_id += 1

        if game:
            roomtype = GameRoom
        else: 
            roomtype = Room
        
        r = roomtype(self.current_id, room_width, room_height, objs=objs)

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
