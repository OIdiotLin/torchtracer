from datetime import datetime

from torchtracer.utils import StoreMan


class Tracer:
    def __init__(self, root):
        self.root = root
        self.storage = None
        print('Tracer start at {}'.format(self.root))

    def attach(self, task_id=None):
        if task_id is None:
            task_id = datetime.now().isoformat(sep='T', timespec='minutes')
        self.storage = StoreMan(self.root, task_id)

    def store(self, item):
        if self.storage is None:
            raise Exception('You should attach first.')
        self.storage.store(item)

    def log(self, msg):
        self.storage.log(msg)
