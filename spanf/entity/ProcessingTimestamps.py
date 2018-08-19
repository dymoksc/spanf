from datetime import datetime

from pony.orm import PrimaryKey, Required

from spanf.utils.globals import db


class ProcessingTimestamps(db.Entity):
    id = PrimaryKey(int)
    timestamp = Required(datetime)
