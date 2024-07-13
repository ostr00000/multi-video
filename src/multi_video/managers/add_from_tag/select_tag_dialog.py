import logging
from pathlib import Path
from typing import TYPE_CHECKING

import more_itertools
from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QDialog, QFileDialog, QListWidgetItem
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.decorators import cursorDecFactory
from pyqt_utils.widgets.base_ui_widget import BaseUiWidget
from pyqt_utils.widgets.tag_filter.dialog import TagFilterDialog
from tag_space_tools.core.tag_finder import TagFinder

from multi_video.model.row import RowGen
from multi_video.qobjects.settings import videoSettings
from multi_video.ui.select_tag_ui import Ui_SelectTagDialog

if TYPE_CHECKING:
    from pyqt_utils.widgets.tag_filter.nodes import TagFilterNode

logger = logging.getLogger(__name__)


class SelectTagDialog(
    Ui_SelectTagDialog, QDialog, BaseUiWidget, metaclass=SlotDecoratorMeta
):
    tagWidget: TagFilterDialog

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self._prepareTagWidget()

        if tagCache := videoSettings.TAG_CACHE:
            self.tagWidget.setPossibleValues(tagCache)

        if lastVal := videoSettings.TAG_DIR:
            self.tagDirLineEdit.setText(lastVal)
            if not tagCache:
                self.onTagDirChanged(lastVal)

        self.changeTagDirButton.clicked.connect(self.onChangeTagDir)
        self.tagDirLineEdit.textChanged.connect(self.onTagDirChanged)
        self.refreshButton.clicked.connect(self.onRefreshButtonClicked)

        self.addButton.clicked.connect(self.onAddTag)
        self.removeButton.clicked.connect(self.onRemoveTag)

        self.listWidget.model().rowsInserted.connect(self.onRowsNumberChanged)
        self.listWidget.model().rowsRemoved.connect(self.onRowsNumberChanged)

    def _prepareTagWidget(self):
        self.tagWidget = TagFilterDialog(parent=self)
        self.tagWidget.setWindowFlag(Qt.Widget)
        self.tagWidget.installEventFilter(self)

        self.tagWidget.buttonBox.hide()

        lay = self.tagWidgetPlaceholder.parentWidget().layout()
        lay.replaceWidget(self.tagWidgetPlaceholder, self.tagWidget)
        self.tagWidgetPlaceholder.hide()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (
            obj is self.tagWidget
            and isinstance(event, QKeyEvent)
            and event.key() == Qt.Key_Escape
        ):
            return True
        return False

    def onChangeTagDir(self):
        baseTagDir = Path(self.tagDirLineEdit.text())

        if not baseTagDir.exists():
            if Path('/home') in baseTagDir.parents:
                while not baseTagDir.exists():
                    baseTagDir = baseTagDir.parent
            else:
                baseTagDir = Path()

        if tagDirectory := QFileDialog.getExistingDirectory(
            self, caption='Select tag root', directory=str(baseTagDir)
        ):
            self.tagDirLineEdit.setText('')  # To send signal
            self.tagDirLineEdit.setText(tagDirectory)

    @cursorDecFactory()
    def onTagDirChanged(self, text):
        if not text:
            return

        try:
            items = TagFinder(text).findAllTags()
        except OSError:
            logger.exception("Cannot find tags")
            return

        videoSettings.TAG_DIR = text
        videoSettings.TAG_CACHE = items
        self.tagWidget.setPossibleValues(items)
        self.listWidget.clear()

    def onRefreshButtonClicked(self):
        self.onTagDirChanged(self.tagDirLineEdit.text())

    def onAddTag(self):
        if tagNode := self.tagWidget.getValue():
            tagNodeRepresentation = repr(tagNode)
            item = QListWidgetItem(tagNodeRepresentation, parent=self.listWidget)
            item.setData(Qt.UserRole, tagNode)
            item.setToolTip(tagNodeRepresentation)

    def onRemoveTag(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

    def onRowsNumberChanged(self):
        self.selectedTagLabel.setText(str(self.listWidget.count()))
        self.removeButton.setEnabled(bool(self.listWidget.count()))

    def getTagFiles(self) -> list[str]:
        if not (tagPath := self.tagDirLineEdit.text()):
            return []

        allowedExt = videoSettings.allowedExtensionsWithDot
        tagFinder = TagFinder(tagPath)
        tagNames = []
        tagsToGen = {}

        for i in range(self.listWidget.count()):
            if (item := self.listWidget.item(i)) is None:
                continue

            tagName = item.text()
            tagFilterNode = item.data(Qt.UserRole) or tagName
            tagNames.append(tagName)
            if tagName not in tagsToGen:
                tagsToGen[tagName] = tagFinder.genFilesWithTag(
                    tagFilterNode, extensions=allowedExt
                )

        genSeq = [tagsToGen[tn] for tn in tagNames]
        tagFiles = []
        for path in more_itertools.roundrobin(*genSeq):
            if (pathStr := str(path)) not in tagFiles:
                tagFiles.append(pathStr)
        return tagFiles

    def genTagGenerators(self):
        dirPath = self.tagDirLineEdit.text()
        for i in range(self.listWidget.count()):
            if (item := self.listWidget.item(i)) is None:
                continue

            tagFilterNode: TagFilterNode = item.data(Qt.UserRole)
            yield RowGen(path=dirPath, tag=tagFilterNode)
