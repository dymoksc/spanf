from datetime import datetime

from pony.orm import db_session, ObjectNotFound, commit, show

from spanf.entities import ProcessingTimestamp


class TimestampManager:
    DATA_PROCESSING_TIMESTAMP_ID = 1  # type: int

    def __init__(self):
        pass

    @db_session
    def updateDataProcessingTimestamp(self, currentTimestamp=datetime.now()):
        # type: (datetime) -> datetime
        try:
            dataProcessingTimestamp = ProcessingTimestamp[self.DATA_PROCESSING_TIMESTAMP_ID]
        except ObjectNotFound:
            dataProcessingTimestamp = ProcessingTimestamp(
                id=self.DATA_PROCESSING_TIMESTAMP_ID,
                timestamp=datetime(1970, 01, 01, 0, 0, 0)
            )
        finally:
            lastTimestamp = dataProcessingTimestamp.timestamp
            dataProcessingTimestamp.timestamp = currentTimestamp

            return lastTimestamp
