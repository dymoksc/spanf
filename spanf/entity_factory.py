from spanf.entities import *
from spanf.no_child_entities_found import NoChildEntitiesFound


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
            try:
                return DataTransformer(path='.', inputDataFormat=next(select(f for f in DataFormat)[:].__iter__()))
            except StopIteration:
                raise NoChildEntitiesFound('DataTransformer entity creation requires at least one DataFormat entity to be already present')

        elif className == 'Client':
            return Client(name='Client name')

        elif className == 'EventType':
            return EventType(name='Event type name')

        elif className == 'DataFormat':
            return DataFormat(mimeType='application/octet-stream', name='Data format name')

        elif className == 'Notifier':
            return Notifier(path='.')

        elif className == 'Sensor':
            try:
                return Sensor(location='Sensor location', client=next(select(c for c in Client)[:].__iter__()))
            except StopIteration:
                raise NoChildEntitiesFound('Sensor entity creation requires at least one Client entity to be already present')

        else:
            raise NotImplementedError
