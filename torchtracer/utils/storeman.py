import os
import json

from torchtracer.data import Config, Model


class StoreMan(object):
    """
    Storage module.
    """
    CONFIG_FILENAME = 'config.json'
    LOG_FILENAME = 'log'

    def __init__(self, root, task_id) -> None:
        super().__init__()
        self.active_log = None
        self.root = root
        self.regist(task_id)

    def regist(self, task_id) -> None:
        dir_path = os.path.abspath(os.path.join(self.root, task_id))
        if os.path.isdir(dir_path):
            raise FileExistsError('{} exists, you should rename the task id.'.format(task_id))
        self.root = self.mkdir(dir_path)

    @staticmethod
    def mkdir(path) -> os.path:
        if not os.path.isdir(path):
            os.mkdir(path)
        return path

    def store(self, item):
        if isinstance(item, Config):
            self.store_config(item)
        elif isinstance(item, Model):
            self.store_model(item)

    def store_config(self, cfg):
        path = os.path.join(self.root, self.CONFIG_FILENAME)
        with open(path, 'w') as f:
            f.write(str(cfg))
            # if isinstance(cfg, dict):
            #     f.write(json.dumps(cfg))
            # else:
            #     raise TypeError('dict needed, but {} found.'.format(type(cfg)))

    def store_model(self, model):
        pass

    def log(self, msg, file=None):
        logfile = os.path.join(self.root,
                               '{}.{}'.format(file, self.LOG_FILENAME) if file else self.LOG_FILENAME)
        if self.active_log:
            if not os.path.basename(self.active_log.name) == logfile:
                self.active_log.close()
                self.active_log = open(logfile, 'a', encoding='utf-8')
        else:
            self.active_log = open(logfile, 'a', encoding='utf-8')
        self.active_log.write(msg + '\n')
