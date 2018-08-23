from datetime import datetime

from pony.orm import db_session, select

from spanf.entities import Data


class DataManager():

    @db_session
    def getDataNewerThan(self, timestamp):
        # type: (datetime) -> list

        return select(d for d in Data if d.timestamp > timestamp)[:]
