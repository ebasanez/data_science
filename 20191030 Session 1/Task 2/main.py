# Objective:  Calculate the rolling of 21 days volatility of any Darwin using less that 1MB of RAM
# TIPS: python chunksizing,pyton io.BytesUI buffers

import sys
import os
import pandas as pd
from classes.fileManager import TmpFileManager
from classes.MemoryManager import MemoryManager

# Common variables
DARWIN_NAME = "LVS"
WINDOW_SIZE = 21
DAY_MILLIS = 86400000

# Read all data set from {PATH_DATA} and perform equivalent process phases to resamble('D') and rolling({WINDOW_SIZE})	
def readAndResample(fileManager):
	
	mem_max = 0
	day_current = 0;
	quote_current = 0;
	for fileStream in fileManager.getDataFilesStreamIterator():
		#pd.read_csv(PATH_DATA+"\\"+f, index_col = 0, chunksize = 1)
		#for df in pd.read_csv(PATH_DATA+"\\"+f, index_col = 0, chunksize = 100):
		with fileStream as file: 
			next(file) # Skip header
			for line in file:
				timestamp_read, quote_read = line.split(',')
				day_read = int(timestamp_read) // DAY_MILLIS
				# If new day is read, last one is persisted as last quote of former day
				if day_read != day_current:
					if day_current != 0:
						fileManager.persistDayLastQuote(day_current, quote_current)
					day_current = day_read
				quote_current = quote_read
				memoryManager.recordMax()
	fileManager.persistDayLastQuote(day_current, quote_current)
	
def rolling(fileManager, window_size):
	line_index = 0
	with fileManager.getDailyQuoteFileStream() as file:
		for line in file:
			for i in range(line_index, line_index + window_size):
				fileManager.persistLineToRollingFile(line, i)
				memoryManager.recordMax()
			line_index += 1

def calculateStd(fileManager, window_size):
	for fileStream in fileManager.getWindowFilesStreamIterator():
		num_lines = 0
		sum = 0
		sum_std = 0
		for line in fileStream:
			# Calculate avg
			quote = line.split(",")[1]
			sum += float(quote)
			num_lines += 1
		# Discard files with less than {window_size} elements	
		if num_lines >= window_size:	
			avg = sum / num_lines	
			memoryManager.recordMax()
			# Reset file read an calculate std deviation
			fileStream.seek(0)
			for line in fileStream:
				quote = line.split(",")[1]
				sum_std += (float(quote)-avg)**2
			last_day = line.split(",")[0]
			std = (sum_std/num_lines)**.5
			fileManager.persistLineToAvgFile(str(last_day)+","+str(std)+"\n")
			memoryManager.recordMax()
		
# Lets do it:
data_path = sys.argv[1]
clean_after_end = (len(sys.argv) > 2 and sys.argv[2] == 'clean')

memoryManager = MemoryManager()
fileManager = TmpFileManager(data_path)
fileManager.createTempFiles()
	
readAndResample(fileManager)
print("Max memory used to resample('D'):", memoryManager.getMax())
rolling(fileManager,WINDOW_SIZE)
print("Max memory used to rolling(WINDOW_SIZE):", memoryManager.getMax())
calculateStd(fileManager,WINDOW_SIZE)
print("Max memory used to calculateStdg(WINDOW_SIZE):", memoryManager.getMax())
