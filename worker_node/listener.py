from google.cloud import pubsub
from google.api_core.exceptions import GoogleAPIError


class Listener:
    def __init__(self, subscription_name, topic, callback):
        """
        Manages Subscription with Google Pub/Sub
        :param subscription_name: name for the listener
        :param topic: topic to subscribe to
        :param callback: method to process messages
        """
        self.subscription_name = subscription_name
        self.topic = topic
        self.callback = callback
        self.subscriber = pubsub.SubscriberClient()
        self.publisher = pubsub.PublisherClient()
        self.__check_topic()
        self.subscription = self.__check_subscription()

    def __check_topic(self):
        """Creates a topic if it doesn't exist"""
        try:
            self.publisher.api.create_topic(self.topic)
        except GoogleAPIError:
            pass

    def __check_subscription(self):
        """Checks if subscription exists else creates one"""
        try:
            return self.subscriber.api.create_subscription(
                self.subscription_name,
                self.topic)
        except GoogleAPIError:
            return self.subscriber.api.get_subscription(self.subscription_name)

    def listen(self):
        """
        Listens to Pipe and executes callback
        :return: future to block main thread
        """
        return self.subscription.open(self.callback)
