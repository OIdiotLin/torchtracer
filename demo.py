import torch
import numpy as np
import torch.nn as nn
from torchtracer import Tracer
from torchtracer.data import Config


def f(x):
    return np.sqrt(x)


def make_batch(batch_size, valid=False):
    if not valid:
        x = np.random.uniform(0, 1000, batch_size)
    else:
        x = np.random.uniform(1000, 2000, batch_size)
    x = x.reshape((batch_size, 1))
    x = torch.Tensor(x)
    y = f(x)
    return x, y


def evaluate(model, **kwargs):
    epoch_n = kwargs['epoch_n']
    batch_size = kwargs['batch_size']
    criterion = kwargs['criterion']

    loss_sum = 0
    for step in range(30):
        x, y = make_batch(batch_size=batch_size)
        y_ = model(x)
        loss = criterion(y, y_)
        loss_sum += loss.item()

    return loss_sum / (30 * batch_size)


def train(model, tracer, **kwargs):
    cfg = Config(kwargs)
    tracer.store(cfg)
    return
    epoch_n = kwargs['epoch_n']
    batch_size = kwargs['batch_size']
    criterion = kwargs['criterion']
    optimizer = kwargs['optimizer']

    train_losses = []
    valid_losses = []

    for epoch in range(epoch_n):
        loss_sum = 0
        for step in range(30):
            x, y = make_batch(batch_size)
            y_ = model(x)
            loss = criterion(y, y_)
            loss_sum += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_loss = loss_sum / (30 * batch_size)
        valid_loss = evaluate(model, **kwargs)

        print(train_loss, valid_loss)

        train_losses.append(train_loss)
        valid_losses.append(valid_loss)


if __name__ == '__main__':
    # with open('./config.ini', 'r') as f:
    #     s = f.read()
    # # cfg = Config(1).from_ini(s)

    net = nn.Sequential(nn.Linear(1, 1, True),
                        # nn.ReLU(),
                        # nn.Linear(6, 12, True),
                        # nn.ReLU(),
                        # nn.Linear(12, 12, True),
                        # nn.ReLU(),
                        # nn.Linear(12, 1, True))
                        )
    args = {'epoch_n': 120,
            'batch_size': 20,
            'criterion': nn.MSELoss(),
            'optimizer': torch.optim.RMSprop(net.parameters(), lr=1e-3)}
    tracer = Tracer('checkpoints')
    tracer.attach()

    train(net, tracer, **args)
