from pony.orm import PrimaryKey, Required, Optional, Set

from spanf.utils.globals import db


class DataTransformer(db.Entity):
    _table_ = 'data_transformer'

    id = PrimaryKey(int, auto=True)
    path = Required(str)
    inputDataFormat = Required('DataFormat', reverse='dataTransformersTakingAsInput', column='input_data_format')
    outputDataFormat = Optional(
        'DataFormat',
        reverse='dataTransformersTakingAsOutput',
        column='output_data_format'
    ) # NULL = event

    producedData = Set('Data')
