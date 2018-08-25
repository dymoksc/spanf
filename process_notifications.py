import logging
from subprocess import Popen, PIPE

from spanf.entities import EventLog, Notifier, db_session
from spanf.logging_level import args
from spanf.timstamp_manager import TimestampManager

# Creating services
logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
timestampManager = TimestampManager()

# Fetching data
logging.info('Getting the last notification processing timestamp')
processingTimestamp = timestampManager.updateTimestamp(TimestampManager.NOTIFICATION_PROCESSING_TIMESTAMP_ID)
logging.info('Timestamp: %s' % processingTimestamp)
eventLogEntriesToProcess = EventLog.getEntriesNewerThan(processingTimestamp)
logging.info('Loaded %d new event log entries' % len(eventLogEntriesToProcess))

# Iterating through event log entries
for eventLog in eventLogEntriesToProcess:  # type: EventLog
    logging.info('Processing EventLog[%d]' % eventLog.id)
    atLeastOneNotificationSent = False

    for notifier in Notifier.getSuitable(eventLog):  # type: Notifier
        logging.info('Notifier[%d]' % notifier.id)
        process = Popen(notifier.path.split() + [str(eventLog.id)], stdin=PIPE, stdout=PIPE)
        process.communicate()
        if process.returncode == 0:
            logging.info('Notified')
            atLeastOneNotificationSent = True
        else:
            logging.info('Notifier has failed')

    if atLeastOneNotificationSent:
        with db_session:
            eventLog = EventLog[eventLog.id]
            eventLog.notified = True
