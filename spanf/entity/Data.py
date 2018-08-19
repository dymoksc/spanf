from pony.orm import PrimaryKey, Required, Optional

from spanf.utils.globals import db


class Data(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(buffer)
    dataFormat = Required('DataFormat', column='data_format')
    producer = Optional('DataTransformer')
    sensor = Required('Sensor')

    precursor = Optional('Data', reverse='successor')
    successor = Optional('Data', reverse='precursor')
