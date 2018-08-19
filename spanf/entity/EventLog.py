from datetime import datetime

from pony.orm import PrimaryKey, Required

from spanf.utils.globals import db


class EventLog(db.Entity):
    _table_ = 'event_log'

    id = PrimaryKey(int, auto=True)
    sensor = Required('Sensor')
    eventType = Required('EventType', column='event_type')
    timestamp = Required(datetime, sql_default='NOW()')
    notified = Required(bool, default=False)