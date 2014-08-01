import time
import os
import datetime
import socket # for hostname
import sys

import server
import foreground
import db
import software_info

IDLE_SECONDS = 60

def run():
    current_foreground = None
    act_sum = 0
    act_count = 0
    def log_action(data):
        nonlocal current_foreground, act_sum, act_count
        application = data[0]
        idle_time = data[1]
        idle = idle_time > IDLE_SECONDS

        if current_foreground and (idle or not current_foreground.application == application):
            current_foreground.duration = (datetime.datetime.now() - current_foreground.start).total_seconds()
            current_foreground.activeness = act_count/act_sum if act_sum>1 else 0

            if current_foreground.duration >= 1 and current_foreground.application != "":
                with db.session_scope() as s:
                    s.add(current_foreground)
                    s.commit()

            current_foreground = None

        if not current_foreground and not idle:
            print(application)
            current_foreground = db.ForegroundApplication(
                application = application,
                start = datetime.datetime.now(),
                hostname = socket.gethostname())
            act_sum = idle_time
            act_count = 1
        else:
            act_sum += idle_time
            act_count += 1

    while(True):
        log_action([foreground.window_name(), foreground.get_idle_duration()])
        time.sleep(.1)




if __name__ == '__main__':
    print("Starting {description} version {version}".format(**software_info.info))
    server.run()
    run()
