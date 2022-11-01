import random

from multi_video.qobjects.settings import videoSettings
from multi_video.window.base import BaseVideoWindow
from pyqt_utils.widgets.time_status_bar import changeStatusDec


class ShuffleManager(BaseVideoWindow):
    def __post_init__(self, *args, **kwargs):
        super().__post_init__(*args, **kwargs)
        self.actionShuffle.triggered.connect(self.onShuffle)

    @changeStatusDec(msg="Data shuffled.")
    def onShuffle(self):
        data = list(self.model)
        random.shuffle(data)
        shuffleInternal = videoSettings.SHUFFLE_INTERNAL_ORDER

        self.model.clean()
        for row in data:
            if shuffleInternal:
                row.shuffle()
            self.model.appendRow(row)

        return True
