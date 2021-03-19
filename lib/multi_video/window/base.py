import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from multi_video.model.video import VideoModel
from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.widget.model_count import ModelCountWidget
from multi_video.ui.ui_multi_video import Ui_MultiVideoMainWindow
from pyqt_settings.action import SettingDialogAction
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.widgets.base_widget import BaseWidget
from pyqt_utils.widgets.time_status_bar import TimeStatusBar

logger = logging.getLogger(__name__)


class BaseVideoWindow(Ui_MultiVideoMainWindow, BaseWidget, QMainWindow,
                      metaclass=SlotDecoratorMeta):

    def __pre_setup__(self, *args, **kwargs):
        super().__pre_setup__(*args, **kwargs)
        self.model = VideoModel(self)
        self.model.dirtyChanged.connect(self.setWindowModified)

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.menuBar().addAction(SettingDialogAction(
            videoSettings, icon=QIcon(), parent=self.menuBar()))

        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(VideoModel.COL_NAME, 400)
        self.tableView.selectionModel().selectionChanged.connect(self._showSelectedCount)

        sb = TimeStatusBar(self)
        sb.addPermanentWidget(ModelCountWidget(self.model))
        self.setStatusBar(sb)

    def _showSelectedCount(self):
        rows = len(self.tableView.selectionModel().selectedRows())
        self.statusBar().showMessage(f"Selected {rows} rows")
