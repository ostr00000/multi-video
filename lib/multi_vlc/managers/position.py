import re
from typing import List

from PyQt5.QtWidgets import QApplication

from multi_vlc.const import ALLOWED_EXTENSIONS
from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.utils.commands import runCommand
from multi_vlc.utils.split_window import calculatePosition, addOffsets
from multi_vlc.vlc_model import Row
from multi_vlc.vlc_window.base import BaseWindow


class PositionManager(BaseWindow):
    VLC_FILE_ARG_PATTERN = re.compile(r'.*vlc.*--started-from-file( \'?.*\.\w+\'?)+')
    FILES_PATTERN = re.compile(r'\'?(.+?\.{ext})\'?'.format(ext='|'.join(ALLOWED_EXTENSIONS)))

    def __post_init__(self):
        super().__post_init__()

        self.actionFind_Opened.triggered.connect(self.onFindOpened)
        self.actionAssign.triggered.connect(self.onRedistribute)

    @changeStatusDec(msg="Found vlc instances.", failureMsg="Not found any vlc.")
    def onFindOpened(self):
        """Find processes vlc - look at '--started-from-file' option"""
        vlcFiles = self.getRunningVlc()
        for file in vlcFiles:
            self.model.appendRow(Row(files=[file]))
        return bool(vlcFiles)

    @changeStatusDec(msg="Configuration redistributed.")
    def onRedistribute(self):
        """Automatically set size and position for vlc"""
        data: List[Row] = list(iter(self.model))

        screen = QApplication.primaryScreen().availableGeometry()
        newPositions = calculatePosition(data, screen.width(), screen.height())
        addOffsets(screen.top(), screen.left(), *newPositions.values())

        self.model.setPositionAndSize(newPositions)
        return True

    @classmethod
    def getRunningVlc(cls) -> List[str]:
        output = runCommand('ps -eo pid,command | grep vlc')
        result = []
        for line in output.split('\n'):
            pid, command = line.split(maxsplit=1)
            match = cls.VLC_FILE_ARG_PATTERN.match(command)
            if match:
                filesStr = match.group(1).lstrip()
                files = cls.FILES_PATTERN.findall(filesStr)
                for f in files:
                    result.append(f)

        return result
