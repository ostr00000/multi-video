import logging
from pprint import pformat

import multi_video.managers
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.python.dynamic_loader import loadClassFromPackage

logger = logging.getLogger(__name__)
# noinspection PyTypeChecker
classes = list(loadClassFromPackage(
    multi_video.managers, requiredSubclass=BaseVideoWindow, logger=logger))


class VideoWindow(*classes, BaseVideoWindow,
                  metaclass=GeometrySaverMeta.wrap(BaseVideoWindow),
                  settings=videoSettings):
    pass


logger.debug(pformat(VideoWindow.mro()))
