import worker.ddocker as ddocker
from time import sleep
#from goto import with_goto
import worker.listener as listener
from enum import Enum

job_name = "name"
file_url = "file"
image_dict = "image"
user_id = "user"

# allow keyboard interrup
import sys, signal
def signal_handler(signal, frame):
    print("\nThank you for choosing dfunc")
    sys.exit(0)

#@with_goto
def main():
    if(not ddocker.dockerExist()):
        print("Please install Docker")
        exit(1)


    try:
        t = ddocker.DockerComputation.computePowerAva()
    except Exception:
        print("Please open Docker daemon before running dFunc")
        exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    print("Exit dfunc with Ctrl+c")
    while (True):
        
        message  = listener.workerMain()

        hello = ddocker.DockerContainer(message['image']['name'],message['image']['tag'])
        hello.run()
        # hello.registerContainer()
    #	print hello.container.logs()
        print hello.get_log()


        #print(hello.get_log())
        #print hello.containerInfo()
        hello.stop()
        # print hello.containerInfo()
        ddocker.DockerQuit.rmAllImage()
        #stats = ddocker.DockerComputation.computeAccumStats()

        #print stats
        
        
if __name__ == "__main__":
    main()