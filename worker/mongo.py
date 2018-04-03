"""
Serach with multi standards
Update feilds for a single item

"""
import pymongo
from pymongo import MongoClient



class MongoInterface:
	
	def __init__(self, connection_string):
		self.pool_size = 2
		self.client = MongoClient(connection_string, maxPoolSize=self.pool_size)

	def get_database(self, db_name):
		return self.client[db_name]

	def getjob_one(self,db_name,collection,cpu,mem):
		query = {"CPU":cpu,
		"MEM":mem}
		result = self.client.db_name.collection.find(query)
		if result.count()>1:
			return result[0]
		return None

	def getjob_first(self,db_name,collection):
		"""Get first job regardless of requirments, Greedy"""
		result = self.client.db_name.collection
		if result.count()>1:
			return result[0]
		return None

	def mark_job(self,db_name,collection,job_id,marking = {}):
		"""Mark a job a Handdeld or Free"""
		return self.client.db_name.collection.update_one({'_id':job_id}, {"$set": marking}, upsert=True)

	def delete_job(self,db_name,collection,job_id):
		"""Delete a job only after it is done"""
		self.client.db_name.collection.delete_one({'_id': job_id})

	@staticmethod
	def getjob_id(jobitem):
		return jobitem['_id']

	@staticmethod
	def getjob_url(jobitem):
		"""
		requires job to have url for download
		"""
		return jobitem['url']

	@staticmethod
	def getjob_image_name(jobitem):
		"""
		requires job to have image_name
		"""
		return jobitem['image_name']
	