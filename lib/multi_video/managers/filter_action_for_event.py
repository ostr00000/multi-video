from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QKeyEvent, QKeySequence
from PyQt5.QtWidgets import QAction

from multi_video.window.base import BaseWindow


class EventFilterForActionManager(BaseWindow):

    def __post_init__(self):
        super().__post_init__()
        self._strShortcutToAction = {}

        for obj in self.__dict__.values():
            if isinstance(obj, QAction):
                for shortcut in obj.shortcuts():
                    self._strShortcutToAction[shortcut.toString().lower()] = obj

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if isinstance(event, QKeyEvent):
            key = QKeySequence(event.modifiers() | event.key()).toString().lower()
            if action := self._strShortcutToAction.get(key):
                action.trigger()

        return super().eventFilter(obj, event)
