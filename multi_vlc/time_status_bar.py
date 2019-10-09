from datetime import datetime

from PyQt5.QtWidgets import QStatusBar


class TimeStatusBar(QStatusBar):
    def showMessage(self, message: str, msecs: int = 0):
        msg = f'{datetime.now().strftime("%H:%M:%S.%f")[:-4]} :  {message}'
        return super().showMessage(msg, msecs)
