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
        self.worker_id = data["worker_id"]
        self.api_d.worker_id = self.worker_id
        path = Config.save("gcreds", data["subscriber_json"], file_type="json")
        Config.put("GOOGLE_APPLICATION_CREDENTIALS", path)
        self.listener = Listener(
            data["subscription_name"], data["subscription_string"], self.run)

    def run(self, message):
        """
        Run this function when
        :param message:
        :return:
        """
        job_id = message['data']
        print(message)
        job_data = self.api_d.initiate_job(job_id)
        docker_data = job_data["image_dict"]
        self.docker.set_image_info(docker_data)
        self.docker.run()
        ip_address = self.docker.get_ip()
        url = "http://{ip_address}:8000/".format(ip_address=ip_address)
        request_data = job_data.setdefault("data", None)
        if request_data:
            response = post(url, json=request_data)
        else:
            response = get(url)
        self.api_d.complete_job(
            job_id, data=response.content, fail=response.ok)
        message.ack()

    def start(self):
        try:
            while True:
                try:
                    future = self.listener.listen()
                    self.api_d.register_worker()
                    future.result()
                except KeyboardInterrupt:
                    exit(0)
                except Exception as e:
                    print(str(e))
                    exit(100)
        except KeyboardInterrupt:
            exit(0)


class WorkerPool:
    def __init__(self):
        self.thread_count = int(Config.get("thread_count", 1))
        self.threads = []
        for each in range(0, self.thread_count):
            w_thread = WorkerThread(each)
            self.threads.append(mp.Process(target=w_thread.start))

    def start(self):
        for thread in self.threads:
            thread.start()

    def kill(self):
        for thread in self.threads:
            thread.terminate()
