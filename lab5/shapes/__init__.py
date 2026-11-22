import importlib
import pkgutil

from .base import Shape, register, registered, create


def load_all():
    for module in pkgutil.iter_modules(__path__):
        if module.name != "base":
            importlib.import_module(f"{__name__}.{module.name}")


load_all()
