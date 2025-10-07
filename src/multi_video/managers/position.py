import re

from PyQt5.QtWidgets import QApplication
from pyqt_utils.widgets.time_status_bar_dec import changeStatusDec

from multi_video.model.row import BaseRow, Row
from multi_video.qobjects.settings import videoSettings
from multi_video.utils.commands import runCommand
from multi_video.utils.split_window import calculatePosition
from multi_video.window.base import BaseVideoWindow


class PositionManager(BaseVideoWindow):
    VLC_FILE_ARG_PATTERN = re.compile(r'.*vlc.*--started-from-file( \'?.*\.\w+\'?)+')

    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.actionFind_Opened.triggered.connect(self.onFindOpened)
        self.actionAssign.triggered.connect(self.onRedistribute)

    @changeStatusDec(msg="Found vlc instances.", failureMsg="Not found any vlc.")
    def onFindOpened(self):
        """Find processes vlc - look at '--started-from-file' option."""
        vlcFiles = self.getRunningVlc()
        for file in vlcFiles:
            self.model.appendRow(Row(files=[file]))
        return bool(vlcFiles)

    @changeStatusDec(msg="Configuration redistributed.")
    def onRedistribute(self):
        """Automatically set size and position for vlc."""
        data: list[BaseRow] = list(iter(self.model))

        screen = QApplication.primaryScreen().availableGeometry()
        newPositions = calculatePosition(data, screen.width(), screen.height())

        marginX = screen.left()
        marginY = screen.top()
        for newPosition in newPositions.values():
            newPosition.move(marginX, marginY)

        self.model.setPositionAndSize(newPositions)
        return True

    @classmethod
    def getRunningVlc(cls) -> list[str]:
        output = runCommand('ps -eo pid,command | grep vlc')
        result: list[str] = []
        for line in output.split('\n'):
            _pid, command = line.split(maxsplit=1)
            if not (match := cls.VLC_FILE_ARG_PATTERN.match(command)):
                continue

            filesStr = match.group(1).lstrip()
            pattern = rf'\'?(.+?\.{"|".join(videoSettings.ALLOWED_EXTENSIONS)})\'?'
            files = re.findall(pattern, filesStr)
            result.extend(files)

        return result
