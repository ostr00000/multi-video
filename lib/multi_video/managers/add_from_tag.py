import logging
from pathlib import Path
from typing import List, Dict, Iterable, TypeVar, Tuple, Sequence

from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QPainter, QColor, QCloseEvent
from PyQt5.QtWidgets import QAction, QToolButton, QDialog, QFileDialog, QInputDialog

from multi_video.model.row import Row
from multi_video.qobjects.settings import videoSettings
from multi_video.ui.ui_select_tag import Ui_SelectTagDialog
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.time_status_bar import changeStatusDec
from tag_space_tools.core.tag_finder import TagFinder

T = TypeVar('T')
U = TypeVar('U')
logger = logging.getLogger(__name__)


class _SelectTagDialog(QDialog, Ui_SelectTagDialog, metaclass=SlotDecoratorMeta):
    TAG_DIR = 'AddFromTag/tagDir'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)

        self.tagDirLineEdit.textChanged.connect(self.onTagDirChanged)
        self.changeTagDirButton.clicked.connect(self.onChangeTagDir)
        self.buttonAdd.clicked.connect(self.onAddTag)
        self.buttonRemove.clicked.connect(self.onRemoveTag)

        if lastVal := videoSettings.TAG_DIR:
            self.tagDirLineEdit.setText(lastVal)

        self.listWidget.currentTextChanged.connect(self.onCurrentTextChanged)

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

    def onTagDirChanged(self, text):
        if not text:
            return

        try:
            items = TagFinder(text).findAllTags()
        except IOError as e:
            logger.error(e)
            return

        videoSettings.TAG_DIR = text
        self.tagComboBox.clear()
        self.tagComboBox.addItems(items)
        self.tagComboBox.setEnabled(True)
        self.buttonAdd.setEnabled(True)
        self.listWidget.clear()

    def onAddTag(self):
        if tagName := self.tagComboBox.currentText():
            self.listWidget.addItem(tagName)

    def onRemoveTag(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))

        if self.listWidget.count() == 0:
            self.buttonRemove.setEnabled(False)

    @pyqtSlot(str)
    def onCurrentTextChanged(self, currentText: str):
        self.buttonRemove.setEnabled(bool(currentText))

    def getTagFiles(self) -> Tuple[List[str], List[str]]:
        if not (tagPath := self.tagDirLineEdit.text()):
            return [], []

        tagFinder = TagFinder(tagPath)
        tagNames = []
        tagsToGen = {}
        for i in range(self.listWidget.count()):
            tagName = self.listWidget.item(i).text()
            tagNames.append(tagName)
            if tagName not in tagsToGen:
                tagsToGen[tagName] = self._genFiles(tagFinder, tagName)

        allowedExt = ['.' + ae for ae in videoSettings.ALLOWED_EXTENSIONS]
        tagFiles = [str(path) for path in self.roundGenerator(tagsToGen, tagNames)
                    if path.suffix in allowedExt]
        return tagFiles, tagNames

    @staticmethod
    def _genFiles(tagFinder: TagFinder, tag: str):
        yield from tagFinder.genFilesWithTag(tag)

    @staticmethod
    def roundGenerator(tagsToGen: Dict[T, Iterable[U]], tagNames: List[T]) -> Iterable[U]:
        tagsToGen = {k: iter(v) for k, v in tagsToGen.items()}
        genSeq = [tagsToGen[tagName] for tagName in tagNames]
        while genSeq:
            firstGen = genSeq.pop(0)
            try:
                yield next(firstGen)
            except StopIteration:
                pass
            else:
                genSeq.append(firstGen)


class AddFromTag(BaseVideoWindow):

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self._createToolButton()
        self._replaceActionToToolButton()
        self._setDefaultAction()

    def _createToolButton(self):
        self.toolButtonAdd = QToolButton(self)
        self.toolButtonAdd.setPopupMode(QToolButton.MenuButtonPopup)

        self.addSingleFromTags = QAction(
            self._getIcon(Qt.red), "Add single from tags", self.toolButtonAdd)
        self.addSingleFromTags.setObjectName('addSingleFromTags')
        self.addSingleFromTags.triggered.connect(self.onAddSingleFromTagTriggered)

        self.addManyFromTags = QAction(
            self._getIcon(Qt.blue), 'Add many from tags', self.toolButtonAdd)
        self.addManyFromTags.setObjectName('addManyFromTags')
        self.addManyFromTags.triggered.connect(self.onAddManyFromTagTriggered)

        self.toolButtonAdd.addAction(self.actionAdd)
        self.toolButtonAdd.addAction(self.addSingleFromTags)
        self.toolButtonAdd.addAction(self.addManyFromTags)

    @staticmethod
    def _getIcon(color: QColor):
        icon = QIcon.fromTheme('list-add')
        pixmap = icon.pixmap(icon.actualSize(QSize(32, 32)))
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        icon = QIcon(pixmap)
        return icon

    def _replaceActionToToolButton(self):
        self.toolBar.insertWidget(self.actionAdd, self.toolButtonAdd)
        self.toolBar.removeAction(self.actionAdd)

    def _setDefaultAction(self):
        objName = videoSettings.TAG_DEFAULT_ACTION
        if not objName:
            objName = self.actionAdd.objectName()

        if not (defaultAction := self.findChild(QAction, objName)):
            defaultAction = self.actionAdd
        self.toolButtonAdd.setDefaultAction(defaultAction)
        self.toolButtonAdd.triggered.connect(self.toolButtonAdd.setDefaultAction)

    def closeEvent(self, closeEvent: QCloseEvent) -> None:
        objName = self.toolButtonAdd.defaultAction().objectName()
        videoSettings.TAG_DEFAULT_ACTION = objName
        super(AddFromTag, self).closeEvent(closeEvent)

    @changeStatusDec(msg="Row from tag files added.")
    def onAddSingleFromTagTriggered(self):
        """Add one row to model from files generated from tags."""
        dlg = _SelectTagDialog(self)
        if dlg.exec_():
            tagFiles, tagNames = dlg.getTagFiles()
            if tagFiles:
                self.model.appendRow(Row(tagFiles))
                return True

    @changeStatusDec(msg="Many rows from tag files added.")
    def onAddManyFromTagTriggered(self):
        """Add many rows to model from files generated from tags."""
        dlg = _SelectTagDialog(self)
        if not dlg.exec_():
            return

        tagFiles, tagNames = dlg.getTagFiles()
        if not tagFiles:
            return

        num, ok = QInputDialog.getInt(
            self, "Video number", "Get number of video row",
            value=min(36, len(tagFiles)), min=1, max=min(144, len(tagFiles)))
        if not ok:
            return

        for tagFilesSeq in self._split(tagFiles, num):
            self.model.appendRow(Row(tagFilesSeq))

        return True

    @staticmethod
    def _split(sequence: Sequence, size: int):
        k, m = divmod(len(sequence), size)
        return (sequence[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
                for i in range(size))
