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
from enum import Enum

# Global Variables
class path(Enum):
    GoogleAPISecretPath = './GoogleAPISecret.json'
    workerAPIkeyPath = './workerAPIkey.json'

class mediator(Enum):
    job_name = "name"
    file_url = "file"
    image_dict = "image"
    user_id = "user"

def setUserkey():
    workerAPIkey = raw_input('Input APIkey (Aquire your APIkey at "http://www.dfunc.tech"):')
    with open(path.workerAPIkeyPath, 'w') as outfile:
        json.dump(workerAPIkey, outfile)
    return workerAPIkey

def setGoogleAPI():
    googleAPIkey = raw_input('Input absolute path (including filename) of Google JSON secret downloaded from "http://www.dfunc.tech" on register):')
    os.rename(googleAPIkey, path.GoogleAPISecretPath)
    if (keyexist(path.GoogleAPISecretPath)):
        getGoogleAPI()

def getGoogleAPI():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(path.GoogleAPISecretPath)

def keyexist(key):
    return os.path.exists(key) 

def getUserkey():
    return json.load(open(path.workerAPIkeyPath))

def receive_messages_with_custom_attributes(project, subscription_name):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        if (message.mediator.file_url!='' and message.mediator.image_dict!=''):
            return message
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)

def workerMain():
    # worker ID 
    if (keyexist(path.workerAPIkeyPath)):
        workerAPIkey = getUserkey()
    else:
        workerAPIkey = setUserkey()
        pass
    print "Your Worker ID: " + workerAPIkey
    # google API secret
    if (keyexist(path.GoogleAPISecretPath)):
        getGoogleAPI()
    else:
        setGoogleAPI()
    # Start listening
    return receive_messages_with_custom_attributes('dfunc',workerAPIkey)




if __name__ == "__main__":
    workerMain()
    #receive_messages("dfunc-bu","what")