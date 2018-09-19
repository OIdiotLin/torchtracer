import os
from datetime import datetime

from torchtracer.utils import StoreMan


class Tracer:
    def __init__(self, root):
        self.root = root
        self.storage = None
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
