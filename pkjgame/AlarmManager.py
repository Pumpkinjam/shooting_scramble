from pkjgame import *
import time

class Alarm:
    '''
    float clock; // once Alarm have been done, clock becomes -1
    float start_time;
    float timing;

    int id;
    '''
    def __init__(self, id, clock):
        self.id = id
        self.clock = clock
        self.start_time = time.time()
        self.timing = self.start_time + self.clock
    
    # return if the valid alarm was done
    def isDone(self) -> bool:
        if self.clock == -1: return False

        if (time.time() > self.timing):
            self.clock = -1
            return True
        else:
            return False
    

    def getPassedTime(self) -> float:
        if self.clock == -1.: return -1.

        tmp = self.timing - time.time()
        if tmp < 0: return -1.
        else: return tmp
        
    
    # reset the start_time and clock (with new_clock)
    def setClock(self, new_clock) -> None:
        self.start_time = time.time()
        self.clock = new_clock
        self.timing = self.start_time + self.clock
    
    # if alarm is done, set Alarm with new_clock and return True
    # else, return False
    def resetAlarm(self, new_clock=None) -> bool:
        if not self.isDone(): return False;

        self.started_time = time.time()
        if new_clock is not None: 
          self.clock = new_clock

        return True


class AlarmManager:

    def __init__(self):
        self.current_id = 0  # primary key for alarms
        self.alarms = dict()
        # self.threads = dict()
    
    def new(self, t=-1): return self.new_alarm(t)
    def new_alarm(self, t=-1) -> Alarm:
        self.current_id += 1
        return self._new_alarm(self.current_id, t)

    def is_done(self, obj_alarm: Alarm) -> bool:
        try:
            return self.alarms[obj_alarm.id].isDone()
        except:
            print('that alarm does not belong to this manager.')
            return None

    def delete(self, obj_alarm: Alarm) -> None:
        obj_alarm.stop()
        del self.alarms[obj_alarm.id]
    
    # do not to call this function directly from the outside of the class
    def _new_alarm(self, id, t) -> Alarm:
        self.alarms[id] = Alarm(id, t)
        return self.alarms[id]

    def get_alarm_list(self) -> list:
        return [_ for _ in self.alarms.values()]