import slave.dfunc_docker as ddocker
from time import sleep



if(ddocker.dockerExist()):	
	t = ddocker.DockerComputation.computePowerAva()
	print(t)
	hello = ddocker.DockerContainer('elasticsearch')
	hello.run()
	# hello.registerContainer()
	sleep(10)
#	print hello.container.logs()
	print hello.get_log()
	#print(hello.get_log())
	#print hello.containerInfo()
	hello.stop()
	# print hello.containerInfo()
	ddocker.DockerQuit.rmAll()
	#stats = ddocker.DockerComputation.computeAccumStats()

	#print stats
	

