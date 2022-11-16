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
        self.objects = dict()       # keys: id (int), values: obj (GameObject)
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.user = UserInfo()

        self.dm.set_background((255, 255, 255, 100))
        self.fps_alarm = self.am.new_alarm(self.spf)
        
        self.create(Player, (60, 60, 32, 32, DisplayManager.get_rectangle_image(32, 32, (0,0,0,100))))
        self.dm.refresh(self.objects.values())
        pass

    def manage(self):
        while True:
            if self.fps_alarm.resetAlarm():
                self.dm.refresh(self.objects.values())


    
    def create(self, cls: type, args: tuple):
        self.object_id += 1
        self.objects[self.object_id] = cls(self.object_id, *args)
    
    def destroy(self, id):
        del self.objects[id]



    class GameEndException(Exception):
        def __init__(self, msg=''):
            print('Game Ended' if msg == '' else msg)
            super().__init__(msg)
        
