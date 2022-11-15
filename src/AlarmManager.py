import threading
import time

# (t)밀리초 후 fun을 실행함
class Alarm:
    
    def __init__(self, t=-1, fun=_empty_fun):
        self.set_timer(t, fun)
    
    def set_timer(self, t, fun=_empty_fun):
        self.started_time = time.time()
        self.timer = t
        self.event = fun
        self.thr = threading.Thread(target=alarm_function)


    def remove(self):
        self.timer = -1
        
    def alarm_function(self):
        time.sleep(self.timer / 1000)
        self.event()

    def _empty_fun():
        pass

    

class AlarmManager:
    current_id = 0  # primary key for alarms

    def __init__(self):
        self.alarms = dict()
        # self.threads = dict()

    def new_alarm(self, fun):
        self.new_alarm(-1, fun)
    
    def new_alarm(self, t, fun):
        current_id += 1
        return _new_alarm(current_id, t, fun)
    
    # strongly recommended not to call this function 
    def _new_alarm(self, id, t, fun):
        self.alarms[id] = Alarm(t, fun)
        return self.alarms[id]