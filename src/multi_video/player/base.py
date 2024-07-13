from abc import ABC, abstractmethod

from multi_video.window.base import BaseVideoWindow


class BasePlayer(ABC):
    def __init__(self, baseWindow: BaseVideoWindow, *args):
        self.baseWindow = baseWindow
        self.model = baseWindow.model
        super().__init__(*args)

    @abstractmethod
    def onStart(self):
        raise NotImplementedError

    @abstractmethod
    def onPause(self, *, isPause: bool):
        raise NotImplementedError

    @abstractmethod
    def onStop(self):
        raise NotImplementedError
