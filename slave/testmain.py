import dfunc_docker as ddocker



if(ddocker.dockerExist()):
	hello = ddocker.DockerContainer('hello-world')
	hello.run()
	print(hello.get_log())
	t = ddocker.DockerComputation.computePowerAva()
	print(t)
	#stats = ddocker.DockerComputation.computeAccumStats()

	print stats
