import more_itertools
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCloseEvent, QColor, QIcon, QPainter
from PyQt5.QtWidgets import QAction, QInputDialog, QToolButton
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.managers.add_from_tag.select_tag_dialog import SelectTagDialog
from multi_video.model.row import Row
from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow


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
            self._getIcon(QColor(Qt.red)), "Add single from tags", self.toolButtonAdd
        )
        self.addSingleFromTags.setObjectName('addSingleFromTags')
        self.addSingleFromTags.triggered.connect(self.onAddSingleFromTagTriggered)

        self.addManyFromTags = QAction(
            self._getIcon(QColor(Qt.blue)), "Add many from tags", self.toolButtonAdd
        )
        self.addManyFromTags.setObjectName('addManyFromTags')
        self.addManyFromTags.triggered.connect(self.onAddManyFromTagTriggered)

        self.addTagGenerator = QAction(
            self._getIcon(QColor('orange')), "Add tag generator", self.toolButtonAdd
        )
        self.addTagGenerator.setObjectName('addTagGenerator')
        self.addTagGenerator.triggered.connect(self.onAddTagGeneratorTriggered)

        self.toolButtonAdd.addAction(self.actionAdd)
        self.toolButtonAdd.addAction(self.addSingleFromTags)
        self.toolButtonAdd.addAction(self.addManyFromTags)
        self.toolButtonAdd.addAction(self.addTagGenerator)

    @staticmethod
    def _getIcon(color: QColor):
        icon = QIcon.fromTheme('list-add')
        pixmap = icon.pixmap(icon.actualSize(QSize(32, 32)))
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return QIcon(pixmap)

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
        super().closeEvent(closeEvent)

    @changeStatusDec(msg="Row from tag files added.")
    def onAddSingleFromTagTriggered(self):
        """Add one row to model from files generated from tags."""
        dlg = SelectTagDialog(self)
        if dlg.exec_():
            tagFiles = dlg.getTagFiles()
            if tagFiles:
                self.model.appendRow(Row(files=tagFiles))
                return True
            return None
        return None

    @changeStatusDec(msg="Many rows from tag files added.")
    def onAddManyFromTagTriggered(self):
        """Add many rows to model from files generated from tags."""
        dlg = SelectTagDialog(self)
        if not dlg.exec_():
            return None

        tagFiles = dlg.getTagFiles()
        if not tagFiles:
            return None

        num, ok = QInputDialog.getInt(
            self,
            "Video number",
            "Get number of video row",
            value=min(36, len(tagFiles)),
            min=1,
            max=min(144, len(tagFiles)),
        )
        if not ok:
            return None

        for tagFilesGen in more_itertools.distribute(num, tagFiles):
            tagFilesSeq = list(tagFilesGen)
            self.model.appendRow(Row(files=tagFilesSeq))

        return True

    @changeStatusDec(msg="Tag generator added.")
    def onAddTagGeneratorTriggered(self):
        if not (dlg := SelectTagDialog(self)).exec_():
            return None

        if not (tagGenerators := list(dlg.genTagGenerators())):
            return None

        for tagGen in tagGenerators:
            self.model.appendRow(tagGen)

        return True
