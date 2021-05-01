import os
import random
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple, Optional, Any

from PyQt5.QtWidgets import QAction, QMenu

from multi_video.qobjects.settings import videoSettings
from pyqt_utils.python.process_async import runProcessAsync
from tag_space_tools.core.tag_finder import TagFinder


class Enum:
    @classmethod
    def getDict(cls):
        return {k: v for k, v in cls.__dict__.items()
                if k.islower() and not k.startswith('_')}


@dataclass
class DataClass(Enum):
    def replace(self, index: int, val):
        k, v = list(self.getDict())[index]
        setattr(self, k, val)


@dataclass
class BaseRow(DataClass):
    hashId: str = field(default_factory=lambda: uuid.uuid4().__str__())
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (0, 0)
    pid: int = -1
    wid: List[int] = field(default_factory=list)

    def __hash__(self):
        return hash(self.hashId)

    @classmethod
    def fromDict(cls, values: dict):
        for sc in cls.__subclasses__():
            try:
                return sc(**values)  # noqa
            except TypeError:
                pass
        raise TypeError(f'Unexpected row type for values: {values}')

    def toDict(self) -> dict[str, Any]:
        return {
            'hashId': self.hashId,
            'position': self.position,
            'size': self.size,
        }

    def __str__(self):
        raise NotImplementedError

    def getContextMenu(self, parentMenu: QMenu) -> Optional[QAction]:
        raise NotImplementedError

    def getFiles(self) -> list[str]:
        raise NotImplementedError

    def shuffle(self):
        pass


class OpenFileFolderAction(QAction):
    def __init__(self, filePath: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filePath = filePath
        self.triggered.connect(self.onTriggered)

    def onTriggered(self):
        runProcessAsync(['xdg-open', self.filePath.parent.absolute().__fspath__()])


@dataclass
class Row(BaseRow):
    files: List[str] = field(default_factory=list)

    def __hash__(self):
        return super().__hash__()

    def shuffle(self):
        random.shuffle(self.files)

    def getFiles(self) -> list[str]:
        return self.files

    def toDict(self):
        return super().toDict() | {'files': self.files}

    def __str__(self):
        return ','.join(map(os.path.basename, self.files))

    def getContextMenu(self, parentMenu: QMenu) -> Optional[QAction]:
        menu = parentMenu.addMenu("Open file folder")

        for filePathStr in self.files:
            filePath = Path(filePathStr)
            action = OpenFileFolderAction(filePath, text=filePath.name, parent=menu)
            menu.addAction(action)
        return menu


@dataclass
class RowGen(BaseRow):
    path: str = ''
    tag: str = ''

    def __hash__(self):
        return super().__hash__()

    def __str__(self):
        return f'Tag[{self.tag}] generator in {self.path}'

    def toDict(self) -> dict[str, Any]:
        return super().getDict() | {'path': self.path, 'tag': self.tag}

    def getContextMenu(self, parentMenu: QMenu) -> Optional[QAction]:
        action = OpenFileFolderAction(
            Path(self.path) / 'child', text="Open root tag folder",
            parent=parentMenu)
        menu = parentMenu.addAction(action)
        return menu

    def getFiles(self) -> list[str]:
        tagFinder = TagFinder(self.path)
        filePaths = tagFinder.genFilesWithTag(self.tag, videoSettings.allowedExtensionsWithDot)
        fileStrings = [str(t) for t in filePaths]
        random.shuffle(fileStrings)
        return fileStrings
