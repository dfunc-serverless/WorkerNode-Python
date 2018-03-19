import pymongo
from pymongo import MongoClient



class MongoInterface:
	
	def __init__(self, connection_string):
		self.pool_size = 2
		self.client = MongoClient(connection_string, maxPoolSize=self.pool_size)

	def get_database(self, db_name):
		return self.client[db_name]