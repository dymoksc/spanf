import logging
from logging_level import args
from subprocess import Popen, PIPE

from pony.orm import db_session, set_sql_debug

from spanf.data_manager import DataManager
from spanf.entities import Data, DataTransformer
from spanf.timstamp_manager import TimestampManager

# Creating services
logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
timestampManager = TimestampManager()
dataManager = DataManager()

logging.info('Getting the last data processing timestamp')
processingTimestamp = timestampManager.updateDataProcessingTimestamp()
logging.info('Timestamp: ' + processingTimestamp.isoformat())
dataToProcess = dataManager.getDataNewerThan(processingTimestamp)
logging.info('Loaded %d new data pieces' % len(dataToProcess))

for data in dataToProcess:  # type: Data
    logging.info('Processing Data[%d]' % data.id)
    for dataTransformer in DataTransformer.getSuitable(data):  # type: DataTransformer
        logging.info('DataTransformer[%d]' % dataTransformer.id)
        process = Popen(dataTransformer.path.split(), stdin=PIPE, stdout=PIPE)
        process.stdin.write(data.content)
        out, err = process.communicate()

        if dataTransformer.outputDataFormat is None:    # Data transformer is an event emitter
            logging.info('event emitter')

        else:                                           # Data transformer outputs another data
            logging.info('Saving output data')
            with db_session:
                Data(
                    content=out,
                    dataFormat=dataTransformer.outputDataFormat.id,
                    producer=dataTransformer.id,
                    sensor=data.sensor.id,
                    precursor=data.id
                )
