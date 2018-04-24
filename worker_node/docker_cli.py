from docker import DockerClient
from docker import errors
from .conf import Config


class DockerException(Exception):
    """Exception in case of Docker errors"""

    def __init__(self, msg=None):
        self.message = msg


class DockerThread:
    """Class to manage docker containers"""

    class __Image:
        """Image class for image metadata"""

        def __init__(self, image_info: dict):
            self.repo = image_info["name"]
            self.tag = image_info["tag"]
            self.command = image_info.setdefault("command", None)
            if {"username", "password"} <= set(image_info):
                self.auth_dict = {
                    "username": image_info["user_name"],
                    "password": image_info["password"]
                }
            else:
                self.auth_dict = None

    def __init__(self):
        base_url = Config.get("docker_base_url", None)
        version = Config.get("docker_version", None)
        tls = Config.get("docker_tls", None)
        if base_url is None:
            self.docker_cli = DockerClient.from_env()
        else:
            self.docker_cli = DockerClient(base_url=base_url,
                                           version=version,
                                           tls=tls)
        self.thread_count = Config.get("thread_count")
        self.image_info: self.__Image = None
        self.image = None
        self.container = None

    def __check_if_info_set(self):
        if self.image_info is None and self.image is None:
            return False
        return True

    def __run_check(self):
        return self.container is None or self.container.status == "exited"

    def set_image_info(self, image_info: dict):
        """
        To set image info, also pulls the image
        :param image_info: image info metadata (dict)
        :return:
        """
        self.image_info = self.__Image(image_info)
        self.pull()

    def pull(self):
        """Pulls image from Registry"""
        if self.__check_if_info_set():
            try:
                self.image = self.docker_cli.images.pull(
                    repository=self.image_info.repo,
                    tag=self.image_info.tag,
                    auth_config=self.image_info.auth_dict
                )
            except errors.ImageNotFound:
                DockerException("Image not found")
        else:
            raise DockerException("Image info not set")

    def run(self):
        """Starts container with predefined command"""
        image = "{repo}:{tag}".format(
            repo=self.image_info.repo,
            tag=self.image_info.tag
        )
        if self.__run_check():
            self.container = self.docker_cli.containers \
                .run(image,
                     self.image_info.command,
                     cpu_period=1000,
                     mem_limit="512m",
                     detach=True)
        else:
            raise DockerException("Container already running")

    def stop(self):
        """Stops the container"""
        if self.__run_check():
            self.container.stop(timeout=5)

    def remove(self):
        """Deletes the container"""
        if self.__run_check():
            self.container.remove(v=True, force=True)
            self.container = None

    def get_ip(self):
        """
        Get's the IP address of attached container
        :return: IP address or None
        """
        if self.__run_check():
            return self.container.attrs['NetworkSettings']['IPAddress']
        return None
