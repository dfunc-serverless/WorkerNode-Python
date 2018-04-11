"""
TODO:
1. Register at http://www.defunc.tech
request
Http GET dfunc.tech/worker/(apikey: from worker user input)
save to relative local place

2. listern
Listening to Server call

Worker ID : subscription_name
msg:  Job ID

3. Run Docker
Get Image name

4. Return result
Send msg
5. Get paid (optional)
dependencies: Docker installed, Python 2.7 or 3.
"""


import argparse
import time
import json
import os.path
from google.cloud import pubsub_v1

import requests
# Global Variables
GoogleAPISecretPath = './SubscribeGoogleSecret.json'
workerCred = './workerCred.json'
curlURL = 'http://localhost:8888/worker/' # publish 'http://www.dfunc.tech/worker/'
job_name = "name"
file_url = "file"
image_dict = "image"
user_id = "user"

# test id 5accf9b83e84b203a54c0c38

# def setUserkey():
#     workerAPIkey = raw_input('Input APIkey (Aquire your APIkey at "http://www.dfunc.tech"):')
#     with open(workerAPIkeyPath, 'w') as outfile:
#         json.dump(workerAPIkey, outfile)
#     return workerAPIkey

def setGoogleAPI(GoogleAPISecret):
    with open(GoogleAPISecretPath, 'w') as outfile:
        json.dump(GoogleAPISecret, outfile)

def getGoogleAPI():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(GoogleAPISecretPath)

def keyexist(key):
    return os.path.exists(key) 

# def getUserkey():
#     return json.load(open(workerCred)).worker_id

def receive_messages_with_custom_attributes(project, subscription_name):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        if (message['']!='' and message['image']!=''):
            return message
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)

def setCredFromWorkerID():
    PARAMS = raw_input('Input APIkey (Aquire your APIkey at "http://www.dfunc.tech"):')
    # workerAPIkey = requests.get(url = 'http://localhost:8888/worker/', params = '5accf9b83e84b203a54c0c38')
    workerAPIkey = requests.get('http://localhost:8888/worker/'+PARAMS).json()

    #print workerAPIkey
    with open(workerCred, 'w') as outfile:
        json.dump(workerAPIkey, outfile)

def getCredFromWorkerID():
    return json.load(open(workerCred))



def workerMain():
    # worker ID 
    if (not keyexist(workerCred)):
        setCredFromWorkerID()
        pass
    workerAPIkey = getCredFromWorkerID()

    # print workerAPIkey['subscriber_json']

    setGoogleAPI(workerAPIkey['subscriber_json'])
    getGoogleAPI()

    # print "Your Worker ID: " + workerAPIkey['worker_id']

    # Start listening
    return receive_messages_with_custom_attributes('dfunc',workerAPIkey['worker_id'])

def reply(message):
    '''send messages back'''
    pass




if __name__ == "__main__":
    workerMain()
    #receive_messages("dfunc-bu","what")
    