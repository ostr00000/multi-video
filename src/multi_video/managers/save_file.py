import logging
from pathlib import Path

from pyqt_utils.widgets.drop_file_dialog import DropFileDialog
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)


class SaveFileManager(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.actionSave_As.triggered.connect(self.onSaveAs)
        self.actionSave.triggered.connect(self.onSave)

    @changeStatusDec(msg="Configuration saved.")
    def onSave(self):
        """Save model to last file."""
        if fileStrPath := videoSettings.LAST_PATH:
            filePath = Path(fileStrPath)
            filePath.write_text(self.model.toJson())
            return True

        self.onSaveAs()
        return None

    @changeStatusDec(msg="Configuration saved.")
    def onSaveAs(self):
        """Save model to new file."""
        fd = DropFileDialog(self, "Save Configuration")
        fd.setNameFilter("Configuration ( *.json )")
        if not fd.exec():
            return None

        filePath = Path(fd.selectedFiles()[0])
        if not filePath.name.endswith('.json'):
            filePath = filePath.with_name(filePath.name + '.json')

        filePath.write_text(self.model.toJson())
        videoSettings.LAST_PATH = str(filePath)
        return True
