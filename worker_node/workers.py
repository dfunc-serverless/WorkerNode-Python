from .conf import Config
from .docker_cli import DockerThread
from .api import API
from .listener import Listener
from requests import get, post

import multiprocessing as mp


class WorkerThread:
    def __init__(self, thread_no: int = 0):
        self.id = thread_no
        self.docker = DockerThread()
        self.api_d = API()
        file_name = "worker_conf-%s" % thread_no
        data = Config.load(file_name)
        if data is None:
            data = self.api_d.create_worker()
            Config.save(file_name, data, file_type="json")
        path = Config.save("gcreds", data["subscriber_json"], file_type="json")
        Config.put("GOOGLE_APPLICATION_CREDENTIALS", path)
        self.listener = Listener(data["subscription_string"],
                                 data["subscription_name"], self.run)

    def run(self, message):
        """
        Run this function when
        :param message:
        :return:
        """
        job_id = message['data']
        job_data = self.api_d.initiate_job(job_id)
        docker_data = job_data["image_dict"]
        self.docker.set_image_info(docker_data)
        self.docker.run()
        ip_address = self.docker.get_ip()
        url = "http://{ip_address}".format(ip_address=ip_address)
        request_data = job_data.setdefault("data", None)
        if request_data:
            response = post(url, json=request_data)
        else:
            response = get(url)
        self.api_d.complete_job(job_id, data=response.content, fail=response.ok)
        message.ack()

    def start(self):
        future = self.listener.listen()
        future.result()


class WorkerPool:
    def __init__(self):
        self.thread_count = Config.get("thread_count", 1)
