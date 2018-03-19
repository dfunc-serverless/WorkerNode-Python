import dfunc_docker as ddocker



if(ddocker.dockerExist()):	
	t = ddocker.DockerComputation.computePowerAva()
	print(t)
	hello = ddocker.DockerContainer('hellow-world')
	hello.run()
	#print(hello.get_log())

	ddocker.DockerQuit.rmAll()
	#stats = ddocker.DockerComputation.computeAccumStats()

	#print stats
	

