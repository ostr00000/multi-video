from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from pyqt_utils.qobjects.display_widget_action import DisplayWidgetAction

from multi_video.window.main import VideoWindow


class PluginVideoAction(DisplayWidgetAction[VideoWindow]):
    sortOrder = 220

    def __init__(self, parent):
        icon = QIcon('multi-video:vlc.svg')
        super().__init__(icon, 'Video', parent)

    def createWidget(self, parent: QWidget | None = None):
        return VideoWindow()
