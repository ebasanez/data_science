import os
import psutil

class MemoryManager:
	
	def __init__(self):
		self.__process = psutil.Process(os.getpid())
		self.__memory_ini = self.__process.memory_info().rss
		self.__memory_max = self.__memory_ini
	
	def recordMax(self):
		self.__memory_max = max(self.__memory_max, self.__process.memory_info().rss)
			
	def getMax(self):
		return (self.__memory_max - self.__memory_ini)/1024