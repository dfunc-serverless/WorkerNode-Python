"""
TODO:connet to docker, 
download image,
run it ,
calcualte compute time,
able to quit,
send STDOUT back to the server

dependencies: Docker installed, Python 2.7 or 3.
"""
import docker

import subprocess
from enum import Enum


class compute(Enum):
	CPU = "NCPU"
	MEM = 'MemTotal'

class globleVar:
	imageName_list = []
	imageID_list = []
	container_list = []
	container_stats = []

client = docker.from_env() # Connect to Docker

class DockerContainer:
	def __init__(self, image_name, tag="latest"):
		self.image_name = image_name
		self.container = None
		self.tag = tag
		client.images.pull("%s:%s" % (image_name, tag))

	def run(self, command=None):
		"""
			Load and run Docker Image
		"""
		if command is None:
			self.container = client.containers.run(self.image_name, detach=True)
		else:
			self.container = client.containers.run(self.image_name, command, detach=True)
			
		globleVar.container_list.append(self.container)
		globleVar.imageName_list.append(self.image_name)
		globleVar.imageID_list.append(self.container.id)

	def containerInfo(self):
		""" Get the information of total Useage"""
		return self.container.stats(stream=False,decode=True)
	

	def stop(self):
		self.container.stop()

	def get_log(self):
		return self.container.logs()

	def get_container(self):
		return self.container
	
	def delete(self):
		self.container.remove(v=True,force=True)


def dockerExist():
	"""
		check if Docker exist
	"""
	command = "docker -v".split()
	return 0 == subprocess.call(command)


# computePowerAva defines images this containner can accomondate
# computePowerUsed claim the price
class DockerComputation:
	def __init__(self, image_ID):
		self.image_name = image_ID
		self.container = None

	@staticmethod
	def computePowerAva():
		"""
		Report comput power based on RAM, CPU, 
		use "Docker Info" equivalent
		"""
		locInfo = client.info()
		#print locInfo
		cpuNmem = []
		if (compute.CPU.value in locInfo and compute.MEM.value in locInfo):
			cpuNmem = [locInfo[compute.CPU.value], locInfo[compute.MEM.value]]
		return cpuNmem

	# @staticmethod
	# def computeAccumStats():
	# 	accumInfo = client.cpu_period()
	# 	return accumInfo

class DockerQuit:
	"""delete images created"""
	@staticmethod
	def rmAllImage():
		for _image_name in  globleVar.imageName_list:
			_id = client.images.get(_image_name).id
			client.images.remove(image=_image_name,force=True)
			# For some reason there are two, this is to delete 
			# the second one that is only able to be deltete by id number
			#client.images.remove(image=_id,force=True) 