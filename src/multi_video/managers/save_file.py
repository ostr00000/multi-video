import logging

from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.widgets.drop_file_dialog import DropFileDialog
from pyqt_utils.widgets.time_status_bar import changeStatusDec

logger = logging.getLogger(__name__)


class SaveFileManager(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionSave.triggered.connect(self.onSave)

    @changeStatusDec(msg="Configuration saved.")
    def onSave(self):
        """Save model to last file"""
        if filePath := videoSettings.LAST_PATH:
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            return True
        else:
            self.onSaveAs()

    @changeStatusDec(msg="Configuration saved.")
    def onSaveAs(self):
        """Save model to new file"""
        fd = DropFileDialog(self, "Save Configuration")
        fd.setNameFilter("Configuration ( *.json )")
        if fd.exec():
            filePath = fd.selectedFiles()[0]
            if not filePath.endswith('.json'):
                filePath += '.json'
            with open(filePath, 'w') as file:
                file.write(self.model.toJson())
            videoSettings.LAST_PATH = filePath
            return True
