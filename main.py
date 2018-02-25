from slave.docker import DockerContainer

if __name__ == "__main__":
	docker = DockerContainer("ubuntu")
	docker.run("echo Hello World")
	print(docker.get_log())
	

