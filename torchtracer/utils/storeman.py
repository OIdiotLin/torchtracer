import os

import torch
from matplotlib.figure import Figure

from torchtracer.data import Config, Model


class StoreMan(object):
    """
    Storage module.
    """
    CONFIG_FILENAME = 'config.json'
    IMG_DIR = 'images'
    MODEL_DESCRIPTION_FILENAME = 'model.txt'
    MODEL_PARAMETERS_FILENAME = 'model.pth'
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

    def close(self):
        self.active_log.close()

    @staticmethod
    def mkdir(path) -> os.path:
        # create task directory
        if not os.path.isdir(path):
            os.mkdir(path)
        # create image directory
        img_dir = os.path.join(path, StoreMan.IMG_DIR)
        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        return path

    def store(self, item, file):
        if isinstance(item, Config):
            self.store_config(item)
        elif isinstance(item, Model):
            self.store_model(item, file)
        elif isinstance(item, Figure):
            self.store_image(item, file)

    def store_config(self, cfg):
        path = os.path.join(self.root, self.CONFIG_FILENAME)
        with open(path, 'w') as f:
            f.write(str(cfg))

    def store_model(self, model, file=None):
        description = str(model)
        parameters = model.state_dict

        description_file = os.path.join(self.root,
                                        '{}.txt'.format(file) if file else self.MODEL_DESCRIPTION_FILENAME)
        parameters_file = os.path.join(self.root,
                                       '{}.pth'.format(file) if file else self.MODEL_PARAMETERS_FILENAME)

        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(description)
        torch.save(parameters, parameters_file)

    def store_image(self, image, file):
        img_file = os.path.join(self.root, self.IMG_DIR, file)
        image.savefig(img_file)

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
