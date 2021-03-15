import logging
from pathlib import Path
from typing import List, Iterable

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from multi_video.model.row import Row
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.python.time_status_bar import changeStatusDec

logger = logging.getLogger(__name__)


class _ExtensionSet:
    def __init__(self, extensions: Iterable[str]):
        self._extensions = set(extensions)

    def __contains__(self, item: str):
        return item in self._extensions or item[1:] in self._extensions


class DropManager(BaseVideoWindow):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self._successDrop = False
        self._allowedExtensions = _ExtensionSet(())

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        """Accept only files"""
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()

        super().dragEnterEvent(a0)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        text = ''
        if int(event.modifiers()) & Qt.ShiftModifier:
            text += f"[SHIFT: no recursion]"
        if int(event.modifiers()) & Qt.ControlModifier:
            text += f"[CTRL: recursion]"
        if int(event.modifiers()) & Qt.AltModifier:
            text += f"[ALT: create multiple records]"

        if text:
            self.statusBar().showMessage(f'drag option: {text}')

        super().keyPressEvent(event)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.statusBar().clearMessage()
        super().keyReleaseEvent(a0)

    @changeStatusDec(msg="Files added.", failureMsg="No files added.", returnValue=False)
    def dropEvent(self, dropEvent: QtGui.QDropEvent):
        """Accept multiple files with allowedExtensions
        or dictionary contains files with these extensions"""
        self._prepareParameters(dropEvent)
        self._successDrop = False
        valid: List[str] = []
        urls = dropEvent.mimeData().urls()

        for url in urls:
            if url.scheme() != 'file':
                continue

            path = Path(url.path())
            if path.is_dir():
                self.loadFromDir(path)
            else:
                if path.suffix in self._allowedExtensions:
                    valid.append(str(path))
                elif path.suffix == 'json' and len(urls) == 1:
                    self._loadConfiguration(path)
                    return

        self.addFiles(valid)

        if not self._successDrop:
            res = super().dropEvent(dropEvent)
            if res is not None:
                return res
        return self._successDrop

    def _prepareParameters(self, dropEvent: QtGui.QDropEvent):
        self._allowedExtensions = _ExtensionSet(videoSettings.ALLOWED_EXTENSIONS)

        if int(dropEvent.keyboardModifiers()) & Qt.ShiftModifier:
            self._recursive = False
        elif int(dropEvent.keyboardModifiers()) & Qt.ControlModifier:
            self._recursive = True
        else:
            self._recursive = videoSettings.DRAG_CREATE_RECURSIVE

        if int(dropEvent.keyboardModifiers()) & Qt.AltModifier:
            self._createOneRow = False
        else:
            self._createOneRow = videoSettings.DRAG_MULTIPLE_CREATE_ONE

    def loadFromDir(self, path: Path):
        validFiles = []
        for file in path.iterdir():
            if file.is_file() and file.suffix in self._allowedExtensions:
                validFiles.append(str(file.absolute()))
            elif self._recursive and file.is_dir():
                self.loadFromDir(file)

        self.addFiles(validFiles)

    def addFiles(self, validFiles: List[str]):
        if not validFiles:
            return

        if self._createOneRow:
            self.model.appendRow(Row(validFiles))

        else:
            for vf in validFiles:
                self.model.appendRow(Row([vf]))

        self._successDrop = True
