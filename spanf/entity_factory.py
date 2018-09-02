from spanf.entities import *


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
            return DataTransformer(path='.', inputDataFormat=next(select(f for f in DataFormat)[:].__iter__()))

        elif className == 'Client':
            return Client(name='Client name')

        elif className == 'EventType':
            return EventType(name='Event type name')

        elif className == 'DataFormat':
            return DataFormat(mimeType='application/octet-stream', name='Data format name')

        elif className == 'Notifier':
            return Notifier(path='.')

        elif className == 'Sensor':
            return Sensor(location='Sensor location', client=next(select(c for c in Client)[:].__iter__()))

        else:
            raise NotImplementedError
