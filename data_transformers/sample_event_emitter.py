"""
Sample event emitting data transformer executable. Regardless of data sent to its STDIN randomly outputs event type or
nothing, simulating two possible logical outcomes of the data evaluation by event emitter.
"""
import sys
from random import randint

EVENT_TYPE_ID = 1

if randint(0, 1):
    sys.stdout.write(str(EVENT_TYPE_ID))
