import logging
import os

from PyQt5 import QtGui

from multi_vlc.const import ALLOWED_EXTENSIONS
from multi_vlc.managers.save_file import SaveFileManager
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.vlc_model import Row

logger = logging.getLogger(__name__)


class DropManager(SaveFileManager):
    def __init__(self, *args):
        super().__init__(*args)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        """Accept only files"""
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()

    @changeStatusDec(msg="Files added.", failureMsg="No files added.", returnValue=False)
    def dropEvent(self, a0: QtGui.QDropEvent):
        """Accept multiple files with ALLOWED_EXTENSIONS
        or dictionary contains files with these extensions"""
        urls = a0.mimeData().urls()
        valid = []

        for url in urls:
            if url.scheme() != 'file':
                continue

            path = url.path()
            if os.path.isdir(path) and len(urls) == 1:
                for file in os.listdir(path):
                    if self.getExtension(file) in ALLOWED_EXTENSIONS:
                        self.model.appendRow(Row([os.path.join(path, file)]))
                return True
            else:
                ext = self.getExtension(path)
                if ext in ALLOWED_EXTENSIONS:
                    valid.append(path)
                elif ext == 'json' and len(urls) == 1:
                    self.loadConfiguration(path)
                    return

        if valid:
            self.model.appendRow(Row(valid))

        return bool(valid)

    @staticmethod
    def getExtension(path: str):
        return os.path.splitext(path)[1][1:].lower()
