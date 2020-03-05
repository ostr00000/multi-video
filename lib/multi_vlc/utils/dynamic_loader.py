import importlib
import logging
import pkgutil
from inspect import isabstract, isclass
from types import ModuleType
from typing import Iterator, Type

logger = logging.getLogger(__name__)


def loadClassFromPackage(package: ModuleType) -> Iterator[Type]:
    for moduleInfo in pkgutil.walk_packages(
            package.__path__, prefix=package.__name__ + '.'):
        try:
            mod: ModuleType = importlib.import_module(moduleInfo.name)
        except ImportError as ie:
            logger.error(str(ie))
        else:
            for maybeClass in mod.__dict__.values():
                if isclass(maybeClass) and not isabstract(maybeClass):
                    if maybeClass.__module__ == moduleInfo.name:
                        logger.debug(f"Found {maybeClass}")
                        yield maybeClass
