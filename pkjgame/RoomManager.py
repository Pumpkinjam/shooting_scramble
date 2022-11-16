from PIL import Image, ImageDraw, ImageFont

class Room:

    def __init__(self, id, room_width, room_height, bg=None, objs=dict()):
        self.id = id
        self.width = room_width
        self.height = room_height
        self.objects = objs        # keys: id (int), values: obj (GameObject)
        self.deleted = False
        if bg is None:
            self.background = Image.new("RGBA", (room_width, room_height))
            ImageDraw.Draw(self.background).rectangle((0, 0, room_width, room_height), (255,255,255,100))
        else:
            self.background = bg

        self.reset_image()

    def reset_image(self) -> None:
        self.image = DisplayManager.image_build(self.width, self.height, self.background, self.objects)
        
    def deep_copy(self):
        return Room(self.id, self.screself.objects.copy())

    def add_object(self, obj):
        self.objects[obj.id] = obj
        self.reset_image()
    
    def del_object(self, obj):
        del self.objects[obj.id]
        self.reset_image()
    
    def get_objects(self):
        return self.objects

    def get_image(self):
        return self.image
    
    
class RoomManager:

    def __init__(self):
        self.current_id = 0
        self.number_rooms = 0
        self.rooms = dict()

        self.first_room = None
        self.current_room = None

    def create_room(self, room_width, room_height, objs=dict()):
        self.number_rooms += 1
        self.current_id += 1
        r = Room(self.current_id, room_width, room_height, objs)

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
            print('goto_room must have at least 1 arguments.')
            raise Exception()
        
        if room_id is None:
            self.current_room = room
        elif room is None:
            self.current_room = self.rooms[room_id]

    class NoRoomException(Exception):
        def __init__(self, msg=''):
            print('No more rooms in RoomManager.' if msg == '' else msg)
            super().__init__(msg)
        
