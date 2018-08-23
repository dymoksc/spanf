from spanf.data_manager import DataManager
from spanf.timstamp_manager import TimestampManager

timestampManager = TimestampManager()
dataManager = DataManager()

processingTimestamp = timestampManager.getDataProcessingTimestamp()
dataToProcess = dataManager.getDataNewerThan(processingTimestamp)