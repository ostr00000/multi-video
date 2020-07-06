import random

from multi_vlc.qobjects.time_status_bar import changeStatusDec
from multi_vlc.vlc_window.base import BaseWindow


class ModelManagement(BaseWindow):
    def __post_init__(self):
        super().__post_init__()

        self.actionShuffle.triggered.connect(self.onShuffle)

    @changeStatusDec(msg="Data shuffled.")
    def onShuffle(self):
        data = list(self.model)
        random.shuffle(data)

        self.model.clean()
        for row in data:
            self.model.appendRow(row)

        return True
