from tqdm import tqdm


class ProgressBar(tqdm):
    def __init__(self, iterable=None, desc=None, total=None, leave=True, file=None, ncols=None, mininterval=0.1,
                 maxinterval=10.0, miniters=None, ascii=None, disable=False, unit='it', unit_scale=False,
                 dynamic_ncols=False, smoothing=0.3, bar_format=None, initial=0, position=None, postfix=None,
                 unit_divisor=1000, gui=False, **kwargs):
        super().__init__(iterable, desc, total, leave, file, ncols, mininterval, maxinterval, miniters, ascii, disable,
                         unit, unit_scale, dynamic_ncols, smoothing, bar_format, initial, position, postfix,
                         unit_divisor, gui, **kwargs)

    def update(self, n=1, **params):
        self.set_postfix(**params)
        super().update(n)
