import slave.dfunc_docker as ddocker

if __name__ == "__main__":
	# docker = DockerContainer("ubuntu")
	# docker.run("echo Hello World")
	# print(docker.get_log())
	hello = ddocker.DockerContainer('hello-world')
	hello.run()
	print(hello.get_log())
	#hello-world
	t = ddocker.DockerComputation.computePowerAva()
	print(t)
	stats = ddocker.DockerComputation.computeAccumStats()


