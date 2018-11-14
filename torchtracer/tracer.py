import os
from datetime import datetime

from tqdm import tqdm

from torchtracer.utils import StoreMan
from torchtracer.utils.progress import ProgressBar


class Tracer:
    def __init__(self, root):
        self.root = root
        self.storage = None
        self.epoch_bar = None
        print('Tracer start at {}'.format(os.path.abspath(self.root)))

    def attach(self, task_id=None):
        if task_id is None:
            task_id = datetime.now().isoformat(sep='T', timespec='minutes')
        self.storage = StoreMan(self.root, task_id)
        print('Tracer attached with task: {}'.format(task_id))
        return self

    def detach(self):
        self.storage.close()

    def store(self, item, file=None):
        if self.storage is None:
            raise Exception('You should attach with task id first.')
        self.storage.store(item, file)

    def log(self, msg, file=None):
        if self.storage is None:
            raise Exception('You should attach with task id first.')
        self.storage.log(msg, file)

    def epoch_bar_init(self, epoch_num):
        self.epoch_bar = ProgressBar(total=epoch_num, desc='Epoch')

    @staticmethod
    def print(msg):
        tqdm.write(msg)
