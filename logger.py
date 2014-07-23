
import time
import foreground
import os

while(True):

    print foreground.window_name()
    print foreground.get_idle_duration()
    time.sleep(.2)


def log_activity(data):
    print data

while(True):
    log_activity([foreground.window_name(), foreground.get_idle_duration()])
    time.sleep(.2)
