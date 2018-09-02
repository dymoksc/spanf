#!/usr/bin/env python

"""
Executable, processing dat in the following steps:
    - fetching all unprocessed data entries accumulated in the database since the last execution
    - applying every applicable data transformer based on the data format and then:
        a) creating another data entry, if the specific data transformer is registered as a data producer, i.e. it has
            a non-null output format
        b) creating a new event log entry, if data transformer is registered as an event emitter, i.e. it has a null
            output format, and returned an event type ID
        c) doing nothing if an event emitter has not returned any event type ID
"""

import logging
from datetime import datetime
from subprocess import Popen, PIPE

from pony.orm import db_session

from spanf.entities import Data, DataTransformer, EventLog
from spanf.logging_level import args
from spanf.timstamp_manager import TimestampManager

# Creating services
logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
timestampManager = TimestampManager()

# Fetching data
logging.info('Getting the last data processing timestamp')
processingTimestamp = timestampManager.updateTimestamp(TimestampManager.DATA_PROCESSING_TIMESTAMP_ID)
logging.info('Timestamp: %s' % processingTimestamp)
dataToProcess = Data.getEntriesNewerThan(processingTimestamp)
logging.info('Loaded %d new data pieces' % len(dataToProcess))

# Iterating through data entries
for data in dataToProcess:  # type: Data
    logging.info('Processing Data[%d]' % data.id)
    for dataTransformer in DataTransformer.getSuitable(data):  # type: DataTransformer
        logging.info('DataTransformer[%d]' % dataTransformer.id)
        process = Popen(dataTransformer.path.split(), stdin=PIPE, stdout=PIPE)
        process.stdin.write(data.content)

        out, err = process.communicate()

        if dataTransformer.outputDataFormat is None:    # Data transformer is an event emitter
            if len(out):
                logging.info('Event detected. EvenType[%d]' % int(out))
                with db_session:
                    EventLog(
                        sensor=data.sensor.id,
                        eventType=int(out),
                        timestamp=datetime.now()
                    )
            else:
                logging.info('No event was detected')

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
