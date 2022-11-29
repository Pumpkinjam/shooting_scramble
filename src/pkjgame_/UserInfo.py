class UserInfo:
    
    filename1 = 'playerInfo.sav'
    filename2 = 'playerDat.sav'

    def __init__(self):
        self.gold = 0
        self.score = 0
        self.high_score = 0
        self.play_time = 0              # int
        self.init_time = time.time()    # float
        
        self.inventory = dict()     # key: str (item's name), value: int (quantity)
        self.item_set = dict()      # key: str (item's place), value: str (item's name)

    def load_file(self):

        with open(UserInfo.filename1, 'r') as f:
            vals = f.readline()
            if not vals: return

            vals = vals.split(', ')
            self.gold = int(vals[0])
            self.score = int(vals[1])
            self.high_score = int(vals[2])
            self.play_time = int(vals[3])
        
        # save inventory data
        with open(UserInfo.filename2, 'r') as f:
            if f.readline() is not line: return

            r = csv.reader(f)
            self.inventory = dict(zip(r[0], r[1]))
            
        print('load complete')
    

    def save_file(self):

        self.play_time += int(time.time() - self.init_time)
        with open(UserInfo.filename1, 'w') as f:
            f.write(self.to_csv_format)
        
        with open(UserInfo.filename2, 'w') as f:
            w = csv.writer(f)
            w.writerow(self.inventory.keys())
            w.writerow(self.inventory.values())

        print('save complete.')
            
    
    # gold, score, high_score, play_time
    def to_csv_format(self):
        return f'{self.gold}, {self.score}, {self.high_score}, {self.play_time}'
    
    def playtime_to_string(self):
        tmp = self.play_time

        SEC_IN_DAY = 60*60*24
        SEC_IN_HOUR = 3600
        SEC_IN_MIN = 60

        d = tmp // SEC_IN_DAY * SEC_IN_DAY
        tmp -= d
        h = tmp // SEC_IN_HOUR * SEC_IN_HOUR
        tmp -= h
        m = tmp // SEC_IN_MIN * SEC_IN_MIN
        tmp -= m
        s = tmp

        return f'{d//SEC_IN_DAY}days, {h//SEC_IN_HOUR}hours {m//SEC_IN_MIN}minutes {s}seconds'