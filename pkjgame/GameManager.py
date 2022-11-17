class GameManager:
    
    def __init__(self, fps, screen_width, screen_height):
        self.fps = fps
        self.spf = 1/fps
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.object_id = 0


    def start(self):
        self.setup()
        try:
            self.manage()
        except:
            return

    def stop(self):
        raise GameManager.GameEndException('Game Stopped.')

    def setup(self):
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.rm = RoomManager(self.screen_width, self.screen_height)
        self.user = UserInfo()
        
        self.rm.create_room(self.screen_width, self.screen_height)
        self.player = self.create(Player, (60, 60, 32, 32, DisplayManager.get_rectangle_image(32, 32, (0,0,0,100))))

        self.fps_alarm = self.am.new_alarm(self.spf)
        
        self.disp()

    def manage(self):
        while True:
            self.player.move(random.randint(-1,1), random.randint(-1,1))
            if self.fps_alarm.resetAlarm():
                self.disp()
                print(self.player.x, self.player.y)
                self.dm.display(self.rm.current_room)
                print(self.fps_alarm.clock)


    def create(self, cls: type, args: tuple):
        return self.rm.current_room.create_object(cls, *args)
    
    def destroy(self, id) -> None:
        del self.objects[id]

    def disp(self) -> None:
        self.dm.display(self.rm.current_room)


    class GameEndException(Exception):
        def __init__(self, msg=''):
            print('Game Ended' if msg == '' else msg)
            super().__init__(msg)
