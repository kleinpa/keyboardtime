import argparse
import datetime
import os
import socket # for hostname
import sys
import time

import server
import foreground
import db
import software_info

IDLE_SECONDS = 60
IGNORE_THRESHOLD = 1

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
            current_foreground.duration = (datetime.datetime.utcnow() - current_foreground.start).total_seconds()
            current_foreground.activeness = act_count/act_sum if act_sum>1 else 0

            if current_foreground.duration >= IGNORE_THRESHOLD and current_foreground.application != "":
                with db.session_scope() as s:
                    s.add(current_foreground)
                    s.commit()

            current_foreground = None

        if not current_foreground and not idle:
            print(application)
            current_foreground = db.ForegroundApplication(
                application = application,
                start = datetime.datetime.utcnow(),
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
    parser = argparse.ArgumentParser(
        description='{description}.'.format(**software_info.info))
    parser.add_argument('--version', action='version',
                        version='{name} {version}'.format(**software_info.info))

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('-s', '--http', help='only run http server', action='store_true')
    mode.add_argument('-l', '--logger', help='only run foreground logger', action='store_true')

    parser.add_argument('-p', '--port', help='only run http server', type=int)

    args = parser.parse_args()

    if not args.logger:
        server.run(args.port)

    if not args.http:
        run()
