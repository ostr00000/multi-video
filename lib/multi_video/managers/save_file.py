import logging

from PyQt5.QtWidgets import QFileDialog
from multi_video.qobjects.settings import settings
from multi_video.qobjects.time_status_bar import changeStatusDec
from multi_video.window.base import BaseWindow

logger = logging.getLogger(__name__)


class SaveFileManager(BaseWindow):

    def __post_init__(self):
        super().__post_init__()

        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionSave.triggered.connect(self.onSave)

    @changeStatusDec(msg="Configuration saved.")
    def onSave(self):
        """Save model to last file"""
        if filePath := settings.LAST_PATH:
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
            settings.LAST_PATH = filePath
            return True
