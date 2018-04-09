import worker.ddocker as ddocker
from time import sleep
#from goto import with_goto


#@with_goto
def main():
    if(ddocker.dockerExist()):	
        try:
            t = ddocker.DockerComputation.computePowerAva()
        except Exception:
            print("Please open Docker daemon before running dFunc")
            exit(1)

        hello = ddocker.DockerContainer('hello-world')
        hello.run()
        # hello.registerContainer()
        sleep(10)
    #	print hello.container.logs()
        print hello.get_log()
        #print(hello.get_log())
        #print hello.containerInfo()
        hello.stop()
        # print hello.containerInfo()
        ddocker.DockerQuit.rmAllImage()
        #stats = ddocker.DockerComputation.computeAccumStats()

        #print stats
    else:
        print("Please install Docker")
        
if __name__ == "__main__":
    main()