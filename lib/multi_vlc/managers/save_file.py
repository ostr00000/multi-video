import logging

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from multi_vlc.qobjects.settings import settings
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.vlc_window.base import BaseWindow

logger = logging.getLogger(__name__)


class SaveFileManager(BaseWindow):
    def __init__(self, *args):
        super().__init__(*args)

        self.lastJson = None
        path = settings.getLastFile()
        if path:
            self.loadConfiguration(path)

    @changeStatusDec(msg="Configuration loaded.")
    def loadConfiguration(self, path):
        try:
            with open(path) as file:
                jsonObj = file.read()
        except OSError as e:
            logger.info(e)
            settings.saveLastFile('')
            return

        self.lastJson = jsonObj
        self.model.loadJson(jsonObj)
        settings.saveLastFile(path)

    def _connectButtons(self):
        super()._connectButtons()

        self.actionNew.triggered.connect(self.onNew)
        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionSave.triggered.connect(self.onSave)
        self.actionLoad.triggered.connect(self.onLoad)
        self.actionReset.triggered.connect(self.onReset)

    def onNew(self):
        """Create new model"""
        self.model.loadJson('[]')

    def onLoad(self):
        """Load model from file"""
        filePath, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )")
        if filePath:
            self.loadConfiguration(filePath)

    @changeStatusDec(msg="Configuration saved.")
    def onSave(self):
        """Save model to last file"""
        filePath = settings.getLastFile()
        if filePath:
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            return True
        else:
            self.onSaveAs()

    @changeStatusDec(msg="Configuration saved.")
    def onSaveAs(self):
        """Save model to new file"""
        filePath, _ext = QFileDialog.getSaveFileName(
            self, "Save Configuration", filter="Configuration ( *.json )")
        if filePath:
            if not filePath.endswith('.json'):
                filePath += '.json'
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            settings.saveLastFile(filePath)
            return True

    @changeStatusDec(msg="Configuration reset.")
    def onReset(self):
        """Reset configuration to last loaded"""
        if self.lastJson:
            self.model.loadJson(self.lastJson)
            return True
        else:
            QMessageBox.warning(self, "Cannot reset",
                                "To reset data must be loaded earlier")
