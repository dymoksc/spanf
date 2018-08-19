from pony.orm import PrimaryKey, Required, Set

from spanf.utils.globals import db


class DataFormat(db.Entity):
    _table_ = 'data_format'

    id = PrimaryKey(int, auto=True)
    name = Required(str)

    data = Set('Data')
    dataTransformersTakingAsInput = Set('DataTransformer', reverse='inputDataFormat')
    dataTransformersTakingAsOutput = Set('DataTransformer', reverse='outputDataFormat')