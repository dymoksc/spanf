from datetime import datetime

from pony.orm import *

db = Database()
db.bind(provider='mysql', host='localhost', user='signal', passwd='signal', db='signal')


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    sensors = Set('Sensor')


class Data(db.Entity):
    id = PrimaryKey(int, auto=True)  # type: int
    content = Required(buffer)  # type: buffer
    dataFormat = Required('DataFormat', column='data_format')  # type: DataFormat
    producer = Optional('DataTransformer')  # type: DataTransformer
    sensor = Required('Sensor')  # type: Sensor
    timestamp = Required(datetime, sql_default='NOW()')  # type: datetime

    precursor = Optional('Data', reverse='successors')  # type: Data
    successors = Set('Data', reverse='precursor')


class DataFormat(db.Entity):
    _table_ = 'data_format'

    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    data = Set('Data')
    dataTransformersTakingAsInput = Set('DataTransformer', reverse='inputDataFormat')
    dataTransformersTakingAsOutput = Set('DataTransformer', reverse='outputDataFormat')


class DataTransformer(db.Entity):
    _table_ = 'data_transformer'

    id = PrimaryKey(int, auto=True)  # type: int
    path = Required(str)  # type: str
    inputDataFormat = Required('DataFormat', reverse='dataTransformersTakingAsInput', column='input_data_format')  # type: DataFormat
    outputDataFormat = Optional(
        'DataFormat',
        reverse='dataTransformersTakingAsOutput',
        column='output_data_format'
    )  # type: DataFormat

    producedData = Set('Data')

    @staticmethod
    @db_session
    def getSuitable(data):
        # type: (Data) -> list
        return select(dt for dt in DataTransformer if dt.inputDataFormat == data.dataFormat)[:]


class EventLog(db.Entity):
    _table_ = 'event_log'

    id = PrimaryKey(int, auto=True)  # type: int
    sensor = Required('Sensor')  # type: Sensor
    eventType = Required('EventType', column='event_type')  # type: EventType
    timestamp = Required(datetime, sql_default='NOW()')  # type: datetime
    notified = Required(bool, default=False)  # type: bool


class EventType(db.Entity):
    _table_ = 'event_type'

    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    loggedEvents = Set('EventLog')


class ProcessingTimestamp(db.Entity):
    _table_ = 'processing_timestamp';

    id = PrimaryKey(int)  # type: int
    timestamp = Required(datetime)  # type: datetime


class Sensor(db.Entity):
    id = PrimaryKey(int, auto=True)  # type: int
    location = Required(str)  # type: str
    client = Required('Client')  # type: Client

    loggedEvents = Set('EventLog')
    data = Set('Data')


db.generate_mapping(create_tables=True)
