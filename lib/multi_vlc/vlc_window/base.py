import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from multi_vlc.qobjects.settings import settings
from multi_vlc.qobjects.time_status_bar import TimeStatusBar
from multi_vlc.ui.ui_vlc import Ui_VlcMainWindow
from multi_vlc.utils.log_metaclass import SlotDecorator
from multi_vlc.vlc_model import VlcModel
from pyqt_settings.action import SettingDialogAction

logger = logging.getLogger(__name__)


class BaseWindow(QMainWindow, Ui_VlcMainWindow,
                 metaclass=SlotDecorator):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.retranslateUi(self)

        self.setStatusBar(TimeStatusBar(self))
        self.menuBar().addAction(SettingDialogAction(
            settings, icon=QIcon(), parent=self.menuBar()))

        self.model = VlcModel(self)
        self.model.dirtyChanged.connect(self.setWindowModified)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(VlcModel.COL_FILES, 400)
        self.tableView.selectionModel().selectionChanged.connect(self._showSelectedCount)

        self.__post_init__()

    def __post_init__(self):
        pass

    def _showSelectedCount(self):
        rows = len(self.tableView.selectionModel().selectedRows())
        self.statusBar().showMessage(f"Selected {rows} rows")
