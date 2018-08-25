from pony.orm import set_sql_debug

from spanf.data_manager import DataManager
from spanf.timstamp_manager import TimestampManager

timestampManager = TimestampManager()
dataManager = DataManager()

set_sql_debug(True)

processingTimestamp = timestampManager.updateDataProcessingTimestamp()
dataToProcess = dataManager.getDataNewerThan(processingTimestamp)
