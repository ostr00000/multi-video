from managers.drop import DropManager
from managers.model_ordering import ModelManagement
from managers.position import PositionManager
from managers.rubber_band import RubberBandManager
from managers.save_file import SaveFileManager
from managers.video import VideoManager
from vlc_window.base import BaseWindow


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
