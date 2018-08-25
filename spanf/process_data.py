from subprocess import Popen, PIPE

from pony.orm import db_session, set_sql_debug

from spanf.data_manager import DataManager
from spanf.entities import Data, DataTransformer
from spanf.timstamp_manager import TimestampManager

# Creating services
timestampManager = TimestampManager()
dataManager = DataManager()


processingTimestamp = timestampManager.updateDataProcessingTimestamp()  # Getting last timestamp and updating in to the current
dataToProcess = dataManager.getDataNewerThan(processingTimestamp)       # Getting list of Data entities to process

for data in dataToProcess:  # type: Data
    for dataTransformer in DataTransformer.getSuitable(data):  # type: DataTransformer
        process = Popen(dataTransformer.path.split(), stdin=PIPE, stdout=PIPE)
        process.stdin.write(data.content)
        out, err = process.communicate()

        with db_session:
            set_sql_debug(True)
            Data(
                content = out,
                dataFormat = dataTransformer.outputDataFormat.id,
                producer = dataTransformer.id,
                sensor = data.sensor.id,
                precursor = data.id
            )