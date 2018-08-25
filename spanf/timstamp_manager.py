from datetime import datetime

from pony.orm import db_session, ObjectNotFound

from spanf.entities import ProcessingTimestamp


class TimestampManager:
    DATA_PROCESSING_TIMESTAMP_ID = 1
    NOTIFICATION_PROCESSING_TIMESTAMP_ID = 2
    ENABLE_AUTO_UPDATE = True

    def __init__(self):
        pass

    @db_session
    def updateTimestamp(self, timestampId, currentTimestamp=datetime.now()):
        # type: (int, datetime) -> datetime
        try:
            processingTimestamp = ProcessingTimestamp[timestampId]
        except ObjectNotFound:
            processingTimestamp = ProcessingTimestamp(
                id=timestampId,
                timestamp=datetime(1970, 01, 01, 0, 0, 0)
            )
        finally:
            # noinspection PyUnboundLocalVariable
            lastTimestamp = processingTimestamp.timestamp
            if self.ENABLE_AUTO_UPDATE:
                processingTimestamp.timestamp = currentTimestamp
            return lastTimestamp
