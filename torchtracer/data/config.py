import configparser
import json

import torch


class Config(object):
    def __init__(self, cfg) -> None:
        super().__init__()
        if isinstance(cfg, configparser.ConfigParser):
            self.content = Config.from_cfg(cfg)
        elif isinstance(cfg, str):
            self.content = Config.from_ini(cfg)
        elif isinstance(cfg, dict):
            self.content = json.dumps(Config.from_dict(cfg), indent=2)

    @staticmethod
    def from_ini(ini):
        config = configparser.ConfigParser()
        config.read_string(ini)
        return Config.from_cfg(config)

    @staticmethod
    def from_cfg(cfg):
        dic = {}
        sections = cfg.sections()
        for section in sections:
            dic_section = {}
            options = cfg.options(section)
            for option in options:
                dic_section[option] = cfg.get(section, option)
            dic[section] = dic_section
        return dic

    @staticmethod
    def from_dict(dic):
        res = {}
        # only loss function name reserved.
        if isinstance(dic, torch.nn.modules.loss._Loss):
            return dic._get_name()
        #
        if isinstance(dic, torch.optim.Optimizer):
            sub = dic.param_groups[0].copy()
            sub.pop('params')
            sub['name'] = dic.__class__.__name__
            return Config.from_dict(sub)
        for k in dic.keys():
            if type(dic[k]) in [int, float, bool, str, list]:
                res[k] = dic[k]
            else:
                res[k] = Config.from_dict(dic[k])
        return res

    def __str__(self):
        return self.content
