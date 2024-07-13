import logging
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.managers.safe_close import SafeCloseManager
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow

logger = logging.getLogger(__name__)


class LoadFileManager(BaseVideoWindow):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)

        self._lastJson = None
        if path := videoSettings.LAST_PATH:
            self._loadConfiguration(Path(path))

        self.actionNew.triggered.connect(self.onNew)
        self.actionLoad.triggered.connect(self.onLoad)
        self.actionReset.triggered.connect(self.onReset)

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    @changeStatusDec(msg="Configuration loaded.")
    def _loadConfiguration(self, path: Path):
        try:
            jsonObj = path.read_text()
        except OSError as e:
            logger.info(e)
            videoSettings.LAST_PATH = ''
            return

        self._lastJson = jsonObj
        self.model.loadJson(jsonObj)
        videoSettings.LAST_PATH = str(path)

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    def onNew(self):
        """Create new model."""
        self.model.loadJson('[]')
        videoSettings.LAST_PATH = ''

    @SafeCloseManager.takeActionIfUnsavedChangesDec
    def onLoad(self):
        """Load model from file."""
        filePath, _ext = QFileDialog.getOpenFileName(
            self, "Load Configuration", filter="Configuration ( *.json )"
        )
        if filePath:
            self._loadConfiguration(Path(filePath))

    @changeStatusDec(msg="Configuration reset.")
    def onReset(self):
        """Reset configuration to last loaded."""
        if self._lastJson:
            self.model.loadJson(self._lastJson)
            return True

        QMessageBox.warning(
            self, "Cannot reset", "To reset data must be loaded earlier"
        )
        return None
