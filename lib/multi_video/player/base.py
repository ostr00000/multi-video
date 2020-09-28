from abc import ABC

from multi_video.window.base import BaseWindow


class BasePlayer(ABC):
    def __init__(self, baseWindow: BaseWindow, *args):
        self.baseWindow = baseWindow
        self.model = baseWindow.model
        super().__init__(*args)

    def onStart(self):
        raise NotImplementedError

    def onPause(self, isPause: bool):
        raise NotImplementedError

    def onStop(self):
        raise NotImplementedError
