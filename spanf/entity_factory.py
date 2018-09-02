from pony.orm import select

from spanf.entities import db, DataFormat, DataTransformer


class EntityFactory:
    def __init__(self):
        pass

    @staticmethod
    def build(className):
        # type: (str) -> db.Entity
        if className == 'DataTransformer':
            return DataTransformer(
                path='.',
                inputDataFormat=next(select(f for f in DataFormat)[:].__iter__())
            )
        else:
            raise NotImplementedError
