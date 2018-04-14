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
        json.dump(GoogleAPISecret, outfile, indent=4)

def getGoogleAPI():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(GoogleAPISecretPath)

def keyexist(key):
    return os.path.exists(key) 

# def getUserkey():
#     return json.load(open(workerCred)).worker_id

def receive_messages_with_custom_attributes(subscription_name, topic, callback):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    try:
        subscription = subscriber.get_subscription(subscription_name)
    except Exception as e:
        subscriber.create_subscription(subscription_name, topic)
    subscription = subscriber.subscribe(subscription_name)

    future = subscription.open(callback)
     
    

def setCredFromWorkerID():
    PARAMS = raw_input('Input APIkey (Aquire your APIkey at "http://www.dfunc.tech"):')
    # workerAPIkey = requests.get(url = 'http://localhost:8888/worker/', params = '5accf9b83e84b203a54c0c38')
    workerAPIkey = requests.get('http://localhost:8888/worker/'+PARAMS).json()

    #print workerAPIkey
    with open(workerCred, 'w') as outfile:
        json.dump(workerAPIkey, outfile, indent=4)

def getCredFromWorkerID():
    return json.load(open(workerCred))

def get_worker_id():
    return getCredFromWorkerID()['worker_id'] 

def get_api_key():
    return getCredFromWorkerID()['subscriber_json']['private_key_id']

def workerMain(callback):
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
    return receive_messages_with_custom_attributes(workerAPIkey["subscription_name"],
                                                workerAPIkey['subscription_string'],
                                                callback)

def reply(message):
    '''send messages back'''

    pass




if __name__ == "__main__":
    pass
    #workerMain()
    #receive_messages("dfunc-bu","what")
    