from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QWidget, QLabel


class ModelCountWidget(QLabel):
    def __init__(self, model: QAbstractItemModel, parent: QWidget = None):
        super().__init__(parent)
        self.model = model
        self.model.rowsInserted.connect(self.onModelChange)
        self.model.modelReset.connect(self.onModelChange)
        self.model.rowsRemoved.connect(self.onModelChange)

        self.onModelChange()

    def onModelChange(self):
        self.setText(f"Total elements: {len(self.model)}")
