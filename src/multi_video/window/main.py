import logging
from pprint import pformat

from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.dynamic_loader import loadClassFromPackage

import multi_video.managers
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)
classes = list(
    loadClassFromPackage(
        multi_video.managers,
        requiredSubclass=BaseVideoWindow,
        logger=logger,
    )
)


class _VideoWindowMeta(GeometrySaverMeta, SlotDecoratorMeta):
    pass


class VideoWindow(  # type: ignore[reportGeneralTypeIssues]
    *classes,
    BaseVideoWindow,
    metaclass=_VideoWindowMeta,
    settings=videoSettings,  # type: ignore[reportCallIssue]
):
    pass


logger.debug(pformat(VideoWindow.mro()))
