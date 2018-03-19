import docker
# https://pypi.python.org/pypi/docker
# http://docker-py.readthedocs.io/en/stable/index.html 
import subprocess

from enum import Enum


# connet to docker, 
# download image
# run it 
# calcualte compute time
# able to quit
# send STDOUT back to the server

# dependencies: Docker installed, Python 2.7 or 3.
# sign in to docker hub


client = docker.from_env() # Connect to Docker

class DockerContainer:
	def __init__(self, image_name):
		self.image_name = image_name
		self.container = None

	def run(self, command=None):
		"""
			Load and run Docker Image
		"""
		if command is None:
			self.container = client.containers.run(self.image_name, detach=True)
		else:
			self.container = client.containers.run(self.image_name, command, detach=True)

	def stop(self):
		self.container.stop()

	def get_log(self):
		return self.container.logs()

	def get_container(self):
		return self.container

	def computeAccumStats(self):
		return self.container.cpu_period(2)


def dockerExist():
	"""
		check if Docker exist
	"""
	command = "docker -v".split()
	return 0 == subprocess.call(command)


class compute(Enum):
	CPU = "NCPU"
	MEM = 'MemTotal'

# computePowerAva defines images this containner can accomondate
# computePowerUsed claim the price
class DockerComputation:
	def __init__(self, image_ID):
		self.image_name = image_name
		self.container = None




	@staticmethod
	def computePowerAva():
		"""
		Report comput power based on RAM, CPU, 
		use "Docker Info" equivalent
		"""
		locInfo = client.info()
		print locInfo
		cpuNmem = []
		if (locInfo.has_key(compute.CPU.value) & locInfo.has_key(compute.MEM.value)):
			cpuNmem = [locInfo[compute.CPU.value], locInfo[compute.MEM.value]]
		return cpuNmem

	# @staticmethod
	# def computeAccumStats():
	# 	accumInfo = client.cpu_period()
	# 	return accumInfo






