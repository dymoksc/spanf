"""
Sample event emitting data transformer executable. Regardless of data sent to its STDIN randomly outputs event type or
nothing, simulating two possible logical outcomes of the data evaluation by event emitter.
"""

from random import randint

EVENT_TYPE_ID = 1

if randint(0, 1):
    print EVENT_TYPE_ID
