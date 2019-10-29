from PyQt5.QtCore import QSettings


class _Settings(QSettings):
    LAST_PATH = 'lastConfig/path'

    def __init__(self):
        super().__init__('MultiVlc', 'multi-vlc')

    def saveLastFile(self, path):
        self.setValue(self.LAST_PATH, path)
        self.sync()

    def getLastFile(self):
        return self.value(self.LAST_PATH, defaultValue=None, type=str)


settings = _Settings()
