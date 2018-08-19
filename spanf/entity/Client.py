from pony.orm import PrimaryKey, Required, Set

from spanf.globals import db


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)

    sensors = Set('Sensor')