from PyQt5.QtCore import QSettings

from multi_vlc import orgName, appName
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.field.string import StrField


class _Settings(QSettings):
    LAST_PATH = StrField('lastConfig/path')
    ASK_TO_SAVE_CHANGED_DATA = BoolField('ask/unsaved', default=True)


settings = _Settings(orgName, appName)
