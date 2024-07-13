from PyQt5.QtWidgets import QLabel, QWidget

from multi_video.model.video import VideoModel


class ModelCountWidget(QLabel):
    def __init__(self, model: VideoModel, parent: QWidget | None = None):
        super().__init__(parent)
        self.model = model
        self.model.rowsInserted.connect(self.onModelChange)
        self.model.modelReset.connect(self.onModelChange)
        self.model.rowsRemoved.connect(self.onModelChange)

        self.onModelChange()

    def onModelChange(self):
        self.setText(f"Total elements: {len(self.model)}")
