import random

from multi_video.qobjects.settings import videoSettings
from multi_video.qobjects.time_status_bar import changeStatusDec
from multi_video.window.base import BaseWindow


class ShuffleManager(BaseWindow):
    def __post_init__(self):
        super().__post_init__()

        self.actionShuffle.triggered.connect(self.onShuffle)

    @changeStatusDec(msg="Data shuffled.")
    def onShuffle(self):
        data = list(self.model)
        random.shuffle(data)
        shuffleInternal = videoSettings.SHUFFLE_INTERNAL_ORDER

        self.model.clean()
        for row in data:
            if shuffleInternal:
                random.shuffle(row.files)
            self.model.appendRow(row)

        return True
