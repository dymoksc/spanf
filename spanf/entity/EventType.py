from pony.orm import PrimaryKey, Required, Set

from spanf.utils.globals import db


class EventType(db.Entity):
    _table_ = 'event_type'

    id = PrimaryKey(int, auto=True)
    name = Required(str)

    loggedEvents = Set('EventLog')