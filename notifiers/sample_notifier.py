import sys
from argparse import ArgumentParser

from pony.orm import db_session

from spanf.entities import EventLog

parser = ArgumentParser()
parser.add_argument('eventLogId', type=int)
args = parser.parse_args()

f = open('/home/gleb/Documents/cvut/sem2/Individualni_projekt/spanf/notifiers/sample_notifier.log', 'a')
with db_session:
    eventLog = EventLog[args.eventLogId]  # type: EventLog
    f.write(
        '[%s] Event of type #%d occurend on sensor %d located at "%s" belonging to client "%s" (%d)\n' %
        (str(eventLog.timestamp), eventLog.eventType.id, eventLog.sensor.id, eventLog.sensor.location,
         eventLog.sensor.client.name, eventLog.sensor.client.id)
    )

f.close()

sys.exit(0)
