from multi_vlc.managers.drop import DropManager
from multi_vlc.managers.model_ordering import ModelManagement
from multi_vlc.managers.position import PositionManager
from multi_vlc.managers.rubber_band import RubberBandManager
from multi_vlc.managers.save_file import SaveFileManager
from multi_vlc.managers.video import VideoManager

from multi_vlc.vlc_window.base import BaseWindow


class VlcWindow(
    DropManager,
    ModelManagement,
    PositionManager,
    RubberBandManager,
    SaveFileManager,
    VideoManager,
    BaseWindow,
):
    pass
