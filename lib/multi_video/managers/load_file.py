import logging

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from multi_video.managers.safe_close import SafeCloseManager
from multi_video.qobjects.settings import settings
from multi_video.qobjects.time_status_bar import changeStatusDec

logger = logging.getLogger(__name__)


class LoadFileManager(SafeCloseManager):
    def __init__(self, *args):
        super().__init__(*args)
        self.lastJson = None

        if path := settings.LAST_PATH:
            self._loadConfiguration(path)

    def __post_init__(self):
        super().__post_init__()

        self.actionNew.triggered.connect(self.onNew)
        self.actionLoad.triggered.connect(self.onLoad)
        self.actionReset.triggered.connect(self.onReset)

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    @changeStatusDec(msg="Configuration loaded.")
    def _loadConfiguration(self, path):
        try:
            with open(path) as file:
                jsonObj = file.read()
        except OSError as e:
            logger.info(e)
            settings.LAST_PATH = ''
            return

        self.lastJson = jsonObj
        self.model.loadJson(jsonObj)
        settings.LAST_PATH = path

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    def onNew(self):
        """Create new model"""
        self.model.loadJson('[]')
        settings.LAST_PATH = ''

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    def onLoad(self):
        """Load model from file"""
        filePath, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )")
        if filePath:
            self._loadConfiguration(filePath)

    @changeStatusDec(msg="Configuration reset.")
    def onReset(self):
        """Reset configuration to last loaded"""
        if self.lastJson:
            self.model.loadJson(self.lastJson)
            return True
        else:
            QMessageBox.warning(self, "Cannot reset",
                                "To reset data must be loaded earlier")
