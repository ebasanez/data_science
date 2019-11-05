import os
from tqdm import tqdm
import shutil

class TmpFileManager:
		
	def __init__(self, dataPath, destroyAtEn = False):
		self.__sep =  os.path.sep
		self.__path_data = dataPath
		self.__destroyAtEnd = destroyAtEn
		self.__path_tmp = os.getcwd() + self.__sep + "tmp" 
		self.__path_rolling = self.__path_tmp + self.__sep + "rolling"
		self.__path_day_quotes = self.__path_tmp + self.__sep + "quotes.csv"
		self.__path_rolling_std = self.__path_tmp + self.__sep + "std.csv"
		self.__path_window_quotes = self.__path_rolling + self.__sep + "window_"
	
	def __del__(self):
		if self.__destroyAtEnd == True:
			self.destroyTempFiles();

	def createTempFiles(self):
		self.destroyTempFiles()
		os.mkdir(self.__path_tmp)
		os.mkdir(self.__path_rolling)
		open(self.__path_day_quotes,'a').close()
	
	def destroyTempFiles(self):
		if os.path.exists(self.__path_tmp):
			shutil.rmtree(self.__path_tmp)

	def persistDayLastQuote(self, day, quote):
		with open(self.__path_day_quotes,'a+') as file:
			file.write(str(day) + "," + str(quote))

	def persistLineToRollingFile(self, line, index):
		with open(self.__path_window_quotes + str(index) + ".csv","a+") as file:
			file.write(line)
		
	def persistLineToAvgFile(self, line):
		with open(self.__path_rolling_std,"a+") as file:
			file.write(line)

	def getDailyQuoteFileStream(self):
		return open(self.__path_day_quotes,'r')
				
	def getDataFilesStreamIterator(self):
		for f in tqdm(os.listdir(self.__path_data)):
			yield open(self.__path_data + f, 'r')

	def getWindowFilesStreamIterator(self):
		for f in tqdm(os.listdir(self.__path_rolling)):
			yield open(self.__path_rolling + self.__sep + f, 'r')

			
			