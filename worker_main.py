import worker.ddocker as ddocker
from time import sleep
#from goto import with_goto
import worker.listener as listener
import requests


job_name = "name"
file_url = "file"
image_dict = "image"
user_id = "user"
curlURL = 'http://localhost:8888/worker/' # publish 'http://www.dfunc.tech/worker/'


# allow keyboard interrup
import sys, signal
def signal_handler(signal, frame):
    '''
    Stuff to do on Exit
    '''
    print("\nThank you for choosing dfunc")
    sys.exit(0)

def dockerHandler(job_id):
    print "we are doing it "
    api_key = listener.get_api_key()
    worker_id = listener.get_worker_id()
    image = requests.get(curlURL+api_key+'/'+worker_id+'/'+job_id).json() # this is the worst structure i every wrote
    
    # hello = ddocker.DockerContainer(image['image']['name'],image['image']['tag'])
    # hello.run()
    # print hello.get_log()
    # hello.stop()
    # ddocker.DockerQuit.rmAllImage()

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
    
    def callback(message):
        print(message)
        print("Runing docker Task")
        pass
        # job_id = message['data'] # get job_id from message
        # print job_id
        # dockerHandler(job_id) # running 
        # message.ack()
    



    signal.signal(signal.SIGINT, signal_handler)
    print("Exit dfunc with Ctrl+c")
    message  = listener.workerMain(callback)

    while (True):
        sleep(100)
        # hello = ddocker.DockerContainer(message['image']['name'],message['image']['tag'])
        # hello.run()
        # hello.registerContainer()
    #	print hello.container.logs()
        # print hello.get_log()


        #print(hello.get_log())
        #print hello.containerInfo()
        # hello.stop()
        # print hello.containerInfo()
        # ddocker.DockerQuit.rmAllImage()
        #stats = ddocker.DockerComputation.computeAccumStats()

        #print stats
        
        
if __name__ == "__main__":
    main()