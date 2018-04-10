import worker.ddocker as ddocker
import worker.listener as listener
from enum import Enum

class mediator(Enum):
    job_name = "name"
    file_url = "file"
    image_dict = "image"
    user_id = "user"


    
if __name__ == "__main__":
    # docker = DockerContainer("ubuntu")
    # docker.run("echo Hello World")
    # print(docker.get_log())
    message  = listener.workerMain()
    hello = ddocker.DockerContainer('hello-world')
    hello.run()
    print(hello.get_log())
    # hello-world
    t = ddocker.DockerComputation.computePowerAva()
    print(t)
#stats = ddocker.DockerComputation.computeAccumStats()
