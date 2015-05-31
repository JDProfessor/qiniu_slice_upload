#!/usr/bin/python

import time

def current_time(plus = 60):
    now = int(time.time())
    deadline = now + plus
    return deadline

deadline = current_time
