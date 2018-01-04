import time
import commands
import os
from lib.eventhook import EventHook

"""
    Representation of the state of the Mac displays.
"""
class Display(object):
    def __init__(self):
        # Setup
        self.onStateChange = EventHook()

    def on(self):
        if self.state == 'OFF':
            os.system("caffeinate -u -t 1")
            time.sleep(0.5)
            self.onStateChange.fire('ON')

    def off(self):
        if self.state == 'ON':
            os.system("pmset displaysleepnow")
            time.sleep(0.5)
            self.onStateChange.fire('OFF')

    # State is a read only property that gets the current status of the displays.
    @property
    def state(self):
        monitorOn = int(commands.getstatusoutput('pmset -g powerstate IODisplayWrangler | tail -1 | cut -c29')[1]) >= 4
        if monitorOn:
            return 'ON'
        else:
            return 'OFF'


