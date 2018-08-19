from pony.orm import set_sql_debug

from spanf.utils.globals import db
# noinspection PyUnresolvedReferences
from spanf.entity import Client, Data, DataFormat, DataTransformer, EventLog, EventType, Sensor

set_sql_debug(True)
db.generate_mapping(create_tables=True)