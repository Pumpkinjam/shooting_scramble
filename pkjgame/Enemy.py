class Enemy(Character):
    
    def __init__(self, room, id, x, y, width, height, image=None):
        super.__init__(room, id, x, y, width, height, image)
        self.drop_rate = 0.3    # or else

    def __del__(self):
        # motion for destructing
        import random as r
        if r.random() < self.drop_rate:
            print('Gold drop!')
            pass # generate gold, item, or else
    
    def act(self, _=None):
        self.move(-5, 0);
    
    def when_collision(self, other):
        pass