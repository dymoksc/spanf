from abc import abstractmethod
from collections import OrderedDict
from datetime import datetime

from pony.orm import *

db = Database()
db.bind(provider='mysql', host='localhost', user='signal', passwd='signal', db='signal')


class ToDictMixin:
    def toDictId(self):
        return OrderedDict(sorted(self.to_dict().iteritems(), key=lambda (k, v): k != 'id'))

    @abstractmethod
    def to_dict(self):
        pass


class Client(db.Entity, ToDictMixin):
    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    sensors = Set('Sensor')
    notifiers = Set('Notifier')


class Data(db.Entity, ToDictMixin):
    id = PrimaryKey(int, auto=True)  # type: int
    content = Required(buffer)  # type: buffer
    dataFormat = Required('DataFormat', column='data_format')  # type: DataFormat
    producer = Optional('DataTransformer')  # type: DataTransformer
    sensor = Required('Sensor')  # type: Sensor
    timestamp = Required(datetime, sql_default='NOW()')  # type: datetime

    precursor = Optional('Data', reverse='successors')  # type: Data
    successors = Set('Data', reverse='precursor')

    @staticmethod
    @db_session
    def getEntriesNewerThan(timestamp):
        # type: (datetime) -> list
        return select(d for d in Data if d.timestamp > timestamp)[:]

    def toDictId(self):
        return OrderedDict(sorted(self.to_dict(exclude=['content']).iteritems(), key=lambda (k, v): k != 'id'))


class DataFormat(db.Entity, ToDictMixin):
    _table_ = 'data_format'

    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    data = Set('Data')
    dataTransformersTakingAsInput = Set('DataTransformer', reverse='inputDataFormat')
    dataTransformersTakingAsOutput = Set('DataTransformer', reverse='outputDataFormat')


class DataTransformer(db.Entity, ToDictMixin):
    _table_ = 'data_transformer'

    id = PrimaryKey(int, auto=True)  # type: int
    path = Required(str)  # type: str
    inputDataFormat = Required('DataFormat', reverse='dataTransformersTakingAsInput',
                               column='input_data_format')  # type: DataFormat
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


class EventLog(db.Entity, ToDictMixin):
    _table_ = 'event_log'

    id = PrimaryKey(int, auto=True)  # type: int
    sensor = Required('Sensor')  # type: Sensor
    eventType = Required('EventType', column='event_type')  # type: EventType
    timestamp = Required(datetime, sql_default='NOW()')  # type: datetime
    notified = Required(bool, default=False)  # type: bool

    @staticmethod
    @db_session
    def getEntriesNewerThan(timestamp):
        # type: (datetime) -> list
        return select(d for d in EventLog if d.timestamp > timestamp)[:]


class EventType(db.Entity, ToDictMixin):
    _table_ = 'event_type'

    id = PrimaryKey(int, auto=True)  # type: int
    name = Required(str)  # type: str

    loggedEvents = Set('EventLog')


class ProcessingTimestamp(db.Entity, ToDictMixin):
    _table_ = 'processing_timestamp';

    id = PrimaryKey(int)  # type: int
    timestamp = Required(datetime)  # type: datetime


class Sensor(db.Entity, ToDictMixin):
    id = PrimaryKey(int, auto=True)  # type: int
    location = Required(str)  # type: str
    client = Required('Client')  # type: Client

    loggedEvents = Set('EventLog')
    data = Set('Data')


class Notifier(db.Entity, ToDictMixin):
    id = PrimaryKey(int, auto=True)  # type: int
    path = Required(str)  # type: str

    clients = Set('Client')

    @staticmethod
    @db_session
    def getSuitable(eventLog):
        # type: (EventLog) -> list[Notifier]
        eventLog = EventLog[eventLog.id]
        return select(n for n in Notifier if eventLog.sensor.client in n.clients)[:]


db.generate_mapping(create_tables=True)
