import gc

class GameManager:
    
    def __init__(self, fps, screen_width, screen_height):
        self.fps = fps
        self.spf = 1/fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.object_id = 0


    def start(self):
        self.setup()
        self.manage()
        '''
        try:
            self.manage()
        except:
            print('what')
            return
            '''

    def stop(self):
        raise GameManager.GameEndException('Game Stopped.')

    def setup(self):
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.rm = RoomManager(self.screen_width, self.screen_height)
        self.joystick = Controller()
        self.user = UserInfo()
        
        
        self.rm.create_room(self.screen_width, self.screen_height)
        self.player = self.create(Player, (60, 60, 32, 32, DisplayManager.get_rectangle_image(32, 32, (0,0,0,255))))

        self.fps_alarm = self.am.new_alarm(self.spf)
        
        self.disp()

    def manage(self):
        
        while True:
            self.rm.current_room.objects_act()
            if self.fps_alarm.resetAlarm():
                self.print_debug()
                self.disp()
                self.player.set_img(DisplayManager.get_rectangle_image(32, 32, (random.randint(0,255), random.randint(0,255), random.randint(0,255), 100)))


    def create(self, cls: type, args: tuple):
        return self.rm.current_room.create_object(cls, args)
    
    def destroy(self, id) -> None:
        del self.objects[id]

    def disp(self) -> None:
        self.dm.display(self.rm.current_room)

    def print_debug(self):
        print(f'current input : {self.joystick.get_input()}')
        print(f'current number of object : {len(self.rm.current_room.objects)}')

    class GameEndException(Exception):
        def __init__(self, msg=''):
            print('Game Ended' if msg == '' else msg)
            super().__init__(msg)