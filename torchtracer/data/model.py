class Model(object):

    def __init__(self, model) -> None:
        super().__init__()
        # print(model)
        self.state_dict = model.state_dict()
        self.name = model.__class__.__name__
        self.architecture = str(model)

    def __str__(self):
        return '{0.name}\n{0.architecture}'.format(self)
