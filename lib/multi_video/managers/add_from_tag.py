from typing import List, Dict, Iterable, TypeVar

from PyQt5.QtCore import QSize, Qt, pyqtSlot, QFile
from PyQt5.QtGui import QIcon, QPainter, QColor, QCloseEvent
from PyQt5.QtWidgets import QAction, QToolButton, QDialog, QFileDialog

from multi_video.model.row import Row
from multi_video.qobjects.settings import videoSettings
from multi_video.ui.ui_select_tag import Ui_SelectTagDialog
from multi_video.window.base import BaseWindow
from pyqt_utils.metaclass.slot_decorator import SlotDecoratorMeta
from pyqt_utils.python.time_status_bar import changeStatusDec
from tag_space_tools.core.tag_search import TagFinder

T = TypeVar('T')
U = TypeVar('U')


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

        if lastVal := videoSettings.value(self.TAG_DIR, defaultValue=''):
            self.tagDirLineEdit.setText(lastVal)

        self.listWidget.currentTextChanged.connect(self.onCurrentTextChanged)

    def onChangeTagDir(self):
        currentTagDir = self.tagDirLineEdit.text()
        directory = currentTagDir if QFile(currentTagDir).exists() else ''

        if tagDirectory := QFileDialog.getExistingDirectory(
                self, caption='Select tag root', directory=directory):
            self.tagDirLineEdit.setText(tagDirectory)

    def onTagDirChanged(self, text):
        if not text:
            return

        videoSettings.setValue(self.TAG_DIR, text)
        items = TagFinder(text).findAllTags()
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

    def getTagRow(self):
        if not (tagPath := self.tagDirLineEdit.text()):
            return

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
        tagRow = Row(tagFiles)
        return tagRow

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


if __name__ == '__main__':
    def _main():
        gens = {1: 'aa', 2: 'bbbbbbbbb', 3: 'ccc'}
        seq = [1, 2, 3, 2, 1]
        res = list(_SelectTagDialog.roundGenerator(gens, seq))
        print(res)


    _main()


class AddFromTag(BaseWindow):
    DEFAULT_ACTION = 'AddFromTag/defaultAction'

    def __init__(self, *args):
        super().__init__(*args)
        self._createToolButton()
        self._replaceActionToToolButton()
        self._setDefaultAction()

    def _createToolButton(self):
        self.toolButtonAdd = QToolButton(self)
        self.toolButtonAdd.setPopupMode(QToolButton.MenuButtonPopup)

        self.addFromTags = QAction(self._getIcon(), 'Add from tags', self.toolButtonAdd)
        self.addFromTags.setObjectName('addFromTags')
        self.addFromTags.triggered.connect(self.onAddFromTagTriggered)
        self.toolButtonAdd.addAction(self.actionAdd)
        self.toolButtonAdd.addAction(self.addFromTags)

    @staticmethod
    def _getIcon():
        color = QColor(Qt.red)
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
        objName = videoSettings.value(
            self.DEFAULT_ACTION, defaultValue=self.actionAdd.objectName())
        if not (defaultAction := self.findChild(QAction, objName)):
            defaultAction = self.actionAdd
        self.toolButtonAdd.setDefaultAction(defaultAction)
        self.toolButtonAdd.triggered.connect(self.toolButtonAdd.setDefaultAction)

    def closeEvent(self, closeEvent: QCloseEvent) -> None:
        objName = self.toolButtonAdd.defaultAction().objectName()
        videoSettings.setValue(self.DEFAULT_ACTION, objName)
        super(AddFromTag, self).closeEvent(closeEvent)

    @changeStatusDec(msg="Tag files added.")
    def onAddFromTagTriggered(self):
        """Add selected tags that generate files to model"""
        dlg = _SelectTagDialog(self)
        if dlg.exec_():
            tagRow = dlg.getTagRow()
            self.model.appendRow(tagRow)
            return True
