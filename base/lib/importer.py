import importlib


def get_attr(cls):
    cls = cls.split(".")
    return getattr(importlib.import_module(".".join(cls[:-1])), cls[-1])


def get_module(cls):
    return importlib.import_module(cls)