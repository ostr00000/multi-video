import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from multi_video.model.video import VideoModel
from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.time_status_bar import TimeStatusBar
from multi_video.qobjects.widget.model_count import ModelCountWidget
from multi_video.ui.ui_multi_video import Ui_MultiVideoMainWindow
from pyqt_settings.action import SettingDialogAction
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta

logger = logging.getLogger(__name__)


class BaseWindow(QMainWindow, Ui_MultiVideoMainWindow,
                 metaclass=SlotDecoratorMeta):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.retranslateUi(self)

        self.menuBar().addAction(SettingDialogAction(
            videoSettings, icon=QIcon(), parent=self.menuBar()))

        self.model = VideoModel(self)
        self.model.dirtyChanged.connect(self.setWindowModified)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(VideoModel.COL_FILES, 400)
        self.tableView.selectionModel().selectionChanged.connect(self._showSelectedCount)

        sb = TimeStatusBar(self)
        sb.addPermanentWidget(ModelCountWidget(self.model))
        self.setStatusBar(sb)

        self.__basePostInit = False
        self.__post_init__()
        assert self.__basePostInit, "You need to call 'super().__post_init__()'"

    def __post_init__(self):
        self.__basePostInit = True

    def _showSelectedCount(self):
        rows = len(self.tableView.selectionModel().selectedRows())
        self.statusBar().showMessage(f"Selected {rows} rows")
