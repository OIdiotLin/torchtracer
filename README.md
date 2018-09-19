# torchtracer

![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/pytorch-0.4.1-orange.svg)

`torchtracer` is a tool package for visualization and storage management in pytorch AI task.

## Getting Started

### PyTorch Required

This tool is developed for PyTorch AI task. Thus, PyTorch is needed of course.

### Installing

You can use `pip` to install `torchtracer`.

```bash
pip install torchtracer
``` 

## How to use?

### Import `torchtracer`

```python
from torchtracer import Tracer
```

### Create an instance of `Tracer`

Assume that the root is `./checkpoints` and current task id is `lmmnb`.

```python
tracer = Tracer('checkpoints').attach('lmmnb')
```

This step will create a directory `checkpoints` inside which is a directory `lmmnb` for current AI task.

### Saving config

Raw config should be a `dict` like this:

```python
# `net` is a defined nn.Module
args = {'epoch_n': 120,
        'batch_size': 10,
        'criterion': nn.MSELoss(),
        'optimizer': torch.optim.RMSprop(net.parameters(), lr=1e-3)}
```

The config dict should be wrapped with `torchtracer.data.Config` when saving it.

```python
cfg = Config(args)
tracer.store(cfg)
```

This step will create `config.json` in `./checkpoints/lmmnb/`, which contains JSON information like this:

```json
{
  "epoch_n": 120,
  "batch_size": 10,
  "criterion": "MSELoss",
  "optimizer": {
    "lr": 0.001,
    "momentum": 0,
    "alpha": 0.99,
    "eps": 1e-08,
    "centered": false,
    "weight_decay": 0,
    "name": "RMSprop"
  }
}
```

### Logging

During the training iteration, you could print any information you want by using `Tracer.log(msg, file)`.

If `file` not specified, it will output `msg` to `./checkpoints/lmmnb/log`. Otherwise, it will be `./checkpoints/lmmnb/something.log`.

```python
tracer.log(msg='Epoch #{:03d}\ttrain_loss: {:.4f}\tvalid_loss: {:.4f}'.format(epoch, train_loss, valid_loss),
           file='losses')
```

This step will create a log file `losses.log` in `./checkpoints/lmmnb/`, which contains logs like:

```text
Epoch #001	train_loss: 18.6356	valid_loss: 21.3882
Epoch #002	train_loss: 19.1731	valid_loss: 17.8482
Epoch #003	train_loss: 19.6756	valid_loss: 19.1418
Epoch #004	train_loss: 20.0638	valid_loss: 18.3875
Epoch #005	train_loss: 18.4679	valid_loss: 19.6304
...
```

### Saving model

The model object should be wrapped with `torchtracer.data.Model`.

```python
tracer.store(Model(model))
```

### Saving matplotlib images

```python
# create figure manually.
plt.plot(train_losses, label='train loss', c='b')
plt.plot(valid_losses, label='valid loss', c='r')
plt.title('Demo Learning on SQRT')
plt.legend()
# save figure.
tracer.store(plt.gcf(), 'losses.png')
```

## Contribute

If you like this project, welcome to pull request & create issues.
