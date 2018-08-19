from pony.orm import PrimaryKey, Required, Set

from spanf.globals import db


class Sensor(db.Entity):
    id = PrimaryKey(int, auto=True)
    location = Required(str)
    client = Required('Client')

    loggedEvents = Set('EventLog')
    data = Set('Data')