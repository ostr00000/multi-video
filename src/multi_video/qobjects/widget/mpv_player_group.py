import logging

from PyQt5.QtCore import QEvent, QObject, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QWidget
from pyqt_utils.metaclass.geometry_saver import GeometrySaverMeta

from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.widget.mpv_player import MpvPlayerWidget, ignoreShutdown
from multi_video.utils.split_window import calculatePosition

logger = logging.getLogger(__name__)


class _FrameWrapper(QFrame):
    def __init__(self, contentWidget: MpvPlayerWidget, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.addWidget(contentWidget)
        self._layout.setContentsMargins(0, 0, 0, 0)

        contentWidget.player.observe_property('mute', self.onMuteChanged)
        self._mute = contentWidget.player.mute
        self.setStyleSheet('QFrame[mute="false"]{ border:1px solid yellow; }')

    @ignoreShutdown
    def onMuteChanged(
        self,
        propertyName: str,
        propertyValue: bool,  # noqa: FBT001 # SKIP mpv API
    ):
        if propertyName != 'mute':
            raise ValueError

        self._mute = propertyValue
        self.setStyleSheet(self.styleSheet())

    def getMute(self):
        return self._mute

    mute = pyqtProperty(bool, getMute)


class MpvPlayerGroupWidget(
    QWidget, metaclass=GeometrySaverMeta, settings=videoSettings
):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._players: dict[int, MpvPlayerWidget] = {}

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyPressEvent(self, event: QKeyEvent):
        match event.key(), self.isFullScreen():
            case Qt.Key_F11 | Qt.Key_Escape, True:
                self.showNormal()
            case Qt.Key_F11, False:
                self.showFullScreen()
            case _:
                super().keyPressEvent(event)

    def createSubWidgets(self, iterable):
        data = list(iterable)
        if not data:
            return

        positions = calculatePosition(data)
        for d in data:
            position = positions[d]
            position.nonNegativeSize()
            self.createSubWidget(
                position.posX, position.posY, position.sizeX, position.sizeY
            )

    def createSubWidget(self, row, column, rowSpan, columnSpan):
        pl = MpvPlayerWidget(self)
        fw = _FrameWrapper(pl, self)
        pl.installEventFilter(self)
        self._players[len(self._players)] = pl
        self._layout.addWidget(fw, row, column, rowSpan, columnSpan)

        logger.debug(f"Created player {id(pl)} [number={len(self._players)}]")

    def playInWidget(self, widgetNumber: int, filenames: list[str]):
        widget = self._players[widgetNumber]
        widget.play(filenames)

    def pause(self, *, isPause: bool):
        for widget in self._players.values():
            widget.setPause(isPause=isPause)

    def closeEvent(self, a0: QCloseEvent) -> None:
        for player in self._players.values():
            player.close()

        self._players.clear()
        super().closeEvent(a0)

    def sizeHint(self) -> QSize:
        return QSize(600, 600)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if (
            isinstance(event, QMouseEvent)
            and event.button() == Qt.MidButton
            and any((player := pl) is obj for pl in self._players.values())
        ):
            player.setMute(change=True)

        return super().eventFilter(obj, event)
