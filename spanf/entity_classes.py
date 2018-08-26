from spanf.entities import *



class EntityClasses:
    _ENTITY_CLASSES_BY_CLASS_NAME = {
        Client.__name__: Client,
        Sensor.__name__: Sensor,
        DataFormat.__name__: DataFormat,
        DataTransformer.__name__: DataTransformer,
        Data.__name__: Data,
        EventType.__name__: EventType,
        EventLog.__name__: EventLog,
        ProcessingTimestamp.__name__: ProcessingTimestamp,
        Notifier.__name__: Notifier,
    }
    
    @staticmethod
    def getClassByName(className):
        # type: (str) -> 'Entity'
        return EntityClasses._ENTITY_CLASSES_BY_CLASS_NAME[className]

    @staticmethod
    def getAllClassNames():
        # type: () -> list[str]
        return EntityClasses._ENTITY_CLASSES_BY_CLASS_NAME.keys()

        