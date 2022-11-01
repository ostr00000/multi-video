from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from multi_video.window.main import VideoWindow
from pyqt_utils.qobjects.display_widget_action import DisplayWidgetAction


class PluginVideoAction(DisplayWidgetAction):
    def __init__(self, parent):
        icon = QIcon(f'multi-video:vlc.svg')
        super().__init__(icon, 'Video', parent)

    def createWidget(self) -> QWidget:
        return VideoWindow()
