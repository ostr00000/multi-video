from decorator import decorator
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox

from multi_video.managers.save_file import SaveFileManager
from multi_video.qobjects.settings import videoSettings


class SafeCloseManager(SaveFileManager):

    @staticmethod
    @decorator
    def takeActionIfUnsavedChangesDec(fun, *args, cancelReturnVal=None, **kwargs):
        self: SafeCloseManager = args[0]
        if self._takeActionIfUnsavedChanges():
            return fun(*args, **kwargs)
        return cancelReturnVal

    def _takeActionIfUnsavedChanges(self):
        """If cancel return False."""
        if not self.model.isDirty:
            return True

        if not videoSettings.ASK_TO_SAVE_CHANGED_DATA:
            return True

        resultButton = QMessageBox.question(
            self,
            "Unsaved changes",
            "Data has been changed. Do you want to save it?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )

        if resultButton == QMessageBox.Save:
            self.onSave()
            return True
        return resultButton == QMessageBox.Discard

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._takeActionIfUnsavedChanges():
            super().closeEvent(event)
        else:
            event.ignore()
