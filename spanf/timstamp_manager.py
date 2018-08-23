from datetime import datetime

from pony.orm import db_session, ObjectNotFound

from spanf.entities import ProcessingTimestamp


class TimestampManager():

    DATA_PROCESSING_TIMESTAMP_ID = 1  # type: int

    @db_session
    def getDataProcessingTimestamp(self):
        # type: () -> datetime
        try:
            return ProcessingTimestamp[self.DATA_PROCESSING_TIMESTAMP_ID]
        except ObjectNotFound:
            return datetime(1970, 01, 01, 0, 0, 0)