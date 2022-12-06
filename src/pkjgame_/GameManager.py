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

    def stop(self):
        raise GameManager.GameEndException('Game Stopped.')

    def setup(self):
        self.am = AlarmManager()
        self.dm = DisplayManager()
        self.rm = RoomManager(self.screen_width, self.screen_height)
        self.joystick = Controller()
        self.user = UserInfo()
        
        
        self.rm.create_room(self.screen_width, self.screen_height, game=True)
        self.rm.current_room.set_enemy_spawn_delay(3)
        self.player = self.create(Player, (60, 180, 32, 32, DisplayManager.get_rectangle_image(32, 32, (50,255,50,100)) ))
        self.boss = self.create(Boss, (0, 170, 30, 120, DisplayManager.get_rectangle_image(30, 120, (255,0,0,100)) ))

        self.fps_alarm = self.am.new_alarm(self.spf)
        
        self.disp()

    def manage(self):
        i=0
        while True:
            if ('B' in self.joystick.get_valid_input()): 
                print('Game End By B key')
                break

            i += 1
            self.rm.current_room.objects_act((self.joystick,))  # every objects in the room acts
                                                                # use joystick if it's needed
            
            # codes in this block are called by fps (every 33ms)
            if self.fps_alarm.resetAlarm():
                #self.print_debug()
                self.disp()


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
