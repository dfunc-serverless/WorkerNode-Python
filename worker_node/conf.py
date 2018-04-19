from json import dumps, loads
import os


class Config:
    path = "./.config"
    __cache = {}

    def __init__(self):
        return

    @classmethod
    def __build_path(cls):
        if not os.path.isdir(cls.path):
            os.mkdir(cls.path)

    @classmethod
    def get_path(cls, name, file_type):
        """
        Build path to config file
        :param name: name of the config
        :param file_type: extension of the file
        :return: path
        """
        return "%s/%s.%s" % (cls.path, name, file_type)

    @classmethod
    def save(cls, name, data, file_type="json", force=False):
        """
        Save configurations to a file
        :param name: name of the config
        :param data: data to be stored
        :param file_type: config type (default: json)
        :param force: force write
        :return: path of the file
        """
        cls.__build_path()
        path = cls.get_path(name, file_type)
        if os.path.isfile(path) and not force:
            return path
        if file_type == "json":
            data = dumps(data, indent=4)
        fl = open(path, 'w')
        fl.write(data)
        fl.close()
        return path

    @classmethod
    def load(cls, name, file_type="json"):
        """
        Load configurations from a file
        :param name: name of the config
        :param file_type: type (default: JSON)
        :return: data or None if file not found
        """
        path = cls.get_path(name, file_type)
        if os.path.isfile(path):
            data = open(path, 'r').read()
            if file_type == "json":
                data = loads(data)
            return data
        return None

    @classmethod
    def get(cls, name, default=None):
        """
        Fetch configurations from Environment variables.
        Pattern: DFUNC_<name of var>
        :param name:
        :param default:
        :return: returns content of the variable
        """
        name = name.upper()
        if name in cls.__cache:
            return cls.__cache[name]
        if name in os.environ:
            val = os.environ[name]
            cls.__cache[name] = val
            return
        elif default is not None:
            return default
        else:
            raise KeyError("Setting %s not found in the environment." % name)

    @classmethod
    def put(cls, name, data):
        """
        Set configurations to environment variable
        :param name: name of the config
        :param data: data to set
        """
        name = name.upper
        os.environ[name] = data
