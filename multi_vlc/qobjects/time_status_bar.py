from datetime import datetime

from PyQt5.QtWidgets import QStatusBar
from decorator import decorator


class TimeStatusBar(QStatusBar):
    def showMessage(self, message: str, msecs: int = 0):
        msg = f'{datetime.now().strftime("%H:%M:%S.%f")[:-4]} :  {message}'
        return super().showMessage(msg, msecs)


@decorator
def changeStatusDec(fun, msg: str = '', failureMsg='', returnValue=1,
                    *args, **kwargs):
    """
    None -> (skip decorator)
    False -> failureMsg
    _ -> msg
    """
    val = fun(*args, **kwargs)
    if val is False:
        msg = failureMsg
    elif val is None:
        return val

    self = args[0]
    try:
        statusBar = self.statusBar()
    except AttributeError:
        statusBar = self.parent().statusBar()

    statusBar.showMessage(msg)
    if returnValue:
        return val
