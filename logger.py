import time
import os
import datetime
import socket # for hostname

import foreground
import db

IDLE_SECONDS = 60

current_action = None
act_sum = 0
act_count = 0
def log_action(data):
    global current_action, act_sum, act_count
    program = data[0]
    idle_time = data[1]
    idle = idle_time > IDLE_SECONDS


    if current_action and (idle or not current_action.program == program):
        current_action.duration = (datetime.datetime.now() - current_action.start).total_seconds()
        current_action.activeness = act_count/act_sum if act_sum>1 else 0

        db.session.add(current_action)
        db.session.commit()

        current_action = None

    if not current_action and not idle:
        print program
        current_action = db.Action(
            program = program,
            start = datetime.datetime.now(),
            hostname = socket.gethostname())
        act_sum = idle_time
        act_count = 1
    else:
        act_sum += idle_time
        act_count += 1

    #print data

while(True):
    log_action([foreground.window_name(), foreground.get_idle_duration()])
    time.sleep(.2)
