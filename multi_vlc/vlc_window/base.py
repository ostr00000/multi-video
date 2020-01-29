import logging

from PyQt5.QtWidgets import QMainWindow

from multi_vlc.qobjects.time_status_bar import TimeStatusBar
from multi_vlc.ui.ui_vlc import Ui_VlcMainWindow
from util.log_metaclass import SlotDecorator
from multi_vlc.vlc_model import VlcModel

logger = logging.getLogger(__name__)


class BaseWindow(QMainWindow, Ui_VlcMainWindow,
                 metaclass=SlotDecorator):

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.retranslateUi(self)

        self.setStatusBar(TimeStatusBar(self))

        self.model = VlcModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(VlcModel.COL_FILES, 400)
        self.tableView.selectionModel().selectionChanged.connect(self._showSelectedCount)

        self._connectButtons()

    def _connectButtons(self):
        pass

    def _showSelectedCount(self):
        rows = len(self.tableView.selectionModel().selectedRows())
        self.statusBar().showMessage(f"Selected {rows} rows")
