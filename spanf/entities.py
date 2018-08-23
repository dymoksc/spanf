from datetime import datetime

from pony.orm import *

set_sql_debug(True)
db = Database()
db.bind(provider='mysql', host='localhost', user='signal', passwd='signal', db='signal')


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)

    sensors = Set('Sensor')


class Data(db.Entity):
    id = PrimaryKey(int, auto=True)
    content = Required(buffer)
    dataFormat = Required('DataFormat', column='data_format')
    producer = Optional('DataTransformer')
    sensor = Required('Sensor')
    timestamp = Required(datetime, sql_default='NOW()')

    precursor = Optional('Data', reverse='successor')
    successor = Optional('Data', reverse='precursor')


class DataFormat(db.Entity):
    _table_ = 'data_format'

    id = PrimaryKey(int, auto=True)
    name = Required(str)

    data = Set('Data')
    dataTransformersTakingAsInput = Set('DataTransformer', reverse='inputDataFormat')
    dataTransformersTakingAsOutput = Set('DataTransformer', reverse='outputDataFormat')


class DataTransformer(db.Entity):
    _table_ = 'data_transformer'

    id = PrimaryKey(int, auto=True)
    path = Required(str)
    inputDataFormat = Required('DataFormat', reverse='dataTransformersTakingAsInput', column='input_data_format')
    outputDataFormat = Optional(
        'DataFormat',
        reverse='dataTransformersTakingAsOutput',
        column='output_data_format'
    )  # NULL = event

    producedData = Set('Data')


class EventLog(db.Entity):
    _table_ = 'event_log'

    id = PrimaryKey(int, auto=True)
    sensor = Required('Sensor')
    eventType = Required('EventType', column='event_type')
    timestamp = Required(datetime, sql_default='NOW()')
    notified = Required(bool, default=False)


class EventType(db.Entity):
    _table_ = 'event_type'

    id = PrimaryKey(int, auto=True)
    name = Required(str)

    loggedEvents = Set('EventLog')


class ProcessingTimestamp(db.Entity):
    _table_ = 'processing_timestamp';

    id = PrimaryKey(int)
    timestamp = Required(datetime)


class Sensor(db.Entity):
    id = PrimaryKey(int, auto=True)
    location = Required(str)
    client = Required('Client')

    loggedEvents = Set('EventLog')
    data = Set('Data')


db.generate_mapping(create_tables=True)
