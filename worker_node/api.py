import requests
from requests.adapters import HTTPAdapter

from .conf import Config


class BadRequestException(Exception):
    """Exception in case of bad request"""

    def __init__(self, msg=None):
        self.message = msg


class API:
    """
    API connector to talk to Scheduler
    """

    def __init__(self):
        """
        Initialises API object
        """
        self.base_uri = Config.get("api_url", "http://localhost:8888")
        self.api_key = Config.get("api_key")
        self.requests = requests.Session()
        self.requests.mount(self.base_uri, HTTPAdapter(max_retries=3))
        self.worker_id = None

    def set_worker_id(self, worker_id):
        """
        Sets local worker id
        :param worker_id:
        """
        self.worker_id = worker_id

    def __get_url(self, path):
        """
        URL builder
        :param path: path to API
        :return:
        """
        return "{0}{1}".format(self.base_uri, path)

    def create_worker(self):
        """
        Registers Worker process
        :return: data related to worker
        """
        path = "/worker/%s" % self.api_key
        url = self.__get_url(path)
        response = self.requests.put(url)
        if response.status_code == 200:
            data = response.json()
            self.set_worker_id(data["worker_id"])
            return data
        else:
            raise BadRequestException(
                "Something went wrong, maybe check the API Key")

    def register_worker(self):
        """
        Registers worker process with scheduler
        :return: updated worker_id
        """
        path = "/worker/{api_key}/{worker_id}".format(
            api_key=self.api_key,
            worker_id=self.worker_id
        )
        url = self.__get_url(path)
        response = self.requests.put(url)
        if response.status_code == 200:
            worker_id = response.json()["worker_id"]
            self.set_worker_id(worker_id)
            return worker_id
        else:
            raise BadRequestException(
                "Something went wrong, maybe check the API Key")

    def register_job(self, job_id):
        """
        Registers job with scheduler
        :param job_id:
        :return:
        """
        path = "/worker/{api_key}/{worker_id}/{job_id}".format(
            api_key=self.api_key,
            worker_id=self.worker_id,
            job_id=job_id
        )
        url = self.__get_url(path)
        response = self.requests.put(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise BadRequestException(
                "Something went wrong, maybe check the API Key")
