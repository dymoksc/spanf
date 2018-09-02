from spanf.entities import *
from spanf.timstamp_manager import TimestampManager


class EntityFactory:
    """
    Used to create valid new entities of all types
    """

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

        elif className == 'Client':
            return Client(
                name='Client name'
            )

        else:
            raise NotImplementedError
