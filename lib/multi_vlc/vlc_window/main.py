import logging
from pprint import pformat

import multi_vlc.managers
from multi_vlc.qobjects.settings import settings
from multi_vlc.vlc_window.base import BaseWindow
from pyqt_settings.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.python.dynamic_loader import loadClassFromPackage

logger = logging.getLogger(__name__)
# noinspection PyTypeChecker
classes = list(loadClassFromPackage(multi_vlc.managers))


class VlcWindow(*classes,
                metaclass=GeometrySaverMeta.wrap(BaseWindow),
                settings=settings):
    pass


logger.debug(pformat(VlcWindow.mro()))
