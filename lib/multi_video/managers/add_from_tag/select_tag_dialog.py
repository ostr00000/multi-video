import logging
from pathlib import Path
from typing import TypeVar, Iterable

import more_itertools
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog

from multi_video.model.row import RowGen
from multi_video.qobjects.settings import videoSettings
from multi_video.ui.select_tag_ui import Ui_SelectTagDialog
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.decorators import cursorDec
from pyqt_utils.widgets.base_widget import BaseWidget
from tag_space_tools.core.tag_finder import TagFinder

T = TypeVar('T')
U = TypeVar('U')
logger = logging.getLogger(__name__)


class SelectTagDialog(Ui_SelectTagDialog, BaseWidget, QDialog, metaclass=SlotDecoratorMeta):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        if tagCache := videoSettings.TAG_CACHE:
            self.setTags(tagCache)

        if lastVal := videoSettings.TAG_DIR:
            self.tagDirLineEdit.setText(lastVal)
            if not tagCache:
                self.onTagDirChanged(lastVal)

        self.tagDirLineEdit.textChanged.connect(self.onTagDirChanged)
        self.changeTagDirButton.clicked.connect(self.onChangeTagDir)
        self.buttonAdd.clicked.connect(self.onAddTag)
        self.buttonRemove.clicked.connect(self.onRemoveTag)
        self.refreshButton.clicked.connect(self.onRefreshButtonClicked)
        self.listWidget.currentTextChanged.connect(self.onCurrentTextChanged)

    def refreshCounter(self):
        self.selectedTagLabel.setText(str(self.listWidget.count()))

    def onChangeTagDir(self):
        baseTagDir = Path(self.tagDirLineEdit.text())

        if not baseTagDir.exists():
            if Path('/home') in baseTagDir.parents:
                while not baseTagDir.exists():
                    baseTagDir = baseTagDir.parent
            else:
                baseTagDir = Path('')

        if tagDirectory := QFileDialog.getExistingDirectory(
                self, caption='Select tag root', directory=str(baseTagDir)):
            self.tagDirLineEdit.setText('')  # To send signal
            self.tagDirLineEdit.setText(tagDirectory)

    def onRefreshButtonClicked(self):
        self.onTagDirChanged(self.tagDirLineEdit.text())

    @cursorDec
    def onTagDirChanged(self, text):
        if not text:
            return

        try:
            items = TagFinder(text).findAllTags()
        except OSError as e:
            logger.error(e)
            return

        videoSettings.TAG_DIR = text
        self.setTags(items)

    def setTags(self, items: list[str]):
        videoSettings.TAG_CACHE = items
        self.tagComboBox.clear()
        self.tagComboBox.addItems(items)
        self.tagComboBox.setEnabled(True)
        self.buttonAdd.setEnabled(True)
        self.listWidget.clear()

    def onAddTag(self):
        if tagName := self.tagComboBox.currentText():
            self.listWidget.addItem(tagName)
            self.refreshCounter()

    def onRemoveTag(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

        if self.listWidget.count() == 0:
            self.buttonRemove.setEnabled(False)
        self.refreshCounter()

    @pyqtSlot(str)
    def onCurrentTextChanged(self, currentText: str):
        self.buttonRemove.setEnabled(bool(currentText))

    def getTagFiles(self) -> tuple[list[str], list[str]]:
        if not (tagPath := self.tagDirLineEdit.text()):
            return [], []

        allowedExt = videoSettings.allowedExtensionsWithDot
        tagFinder = TagFinder(tagPath)
        tagNames = []
        tagsToGen = {}

        for i in range(self.listWidget.count()):
            tagName = self.listWidget.item(i).text()
            tagNames.append(tagName)
            if tagName not in tagsToGen:
                tagsToGen[tagName] = tagFinder.genFilesWithTag(tagName, extensions=allowedExt)

        genSeq = [tagsToGen[tagName] for tagName in tagNames]
        tagFiles = [str(path) for path in more_itertools.roundrobin(*genSeq)]
        return tagFiles, tagNames

    def genTagGenerators(self) -> Iterable[RowGen]:
        dirPath = self.tagDirLineEdit.text()
        for i in range(self.listWidget.count()):
            tag = self.listWidget.item(i).text()
            yield RowGen(path=dirPath, tag=tag)
