from PyQt5.QtCore import QSettings

from multi_vlc import orgName, appName
from pyqt_settings.factory.base import InitArgWidgetFactory
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.field.string import StrField
from pyqt_settings.gui_widget.combo_box import ComboBoxFieldWidget


class _Settings(QSettings):
    LAST_PATH = StrField('lastConfig/path')
    ASK_TO_SAVE_CHANGED_DATA = BoolField('ask/unsaved', default=True)

    VIDEO_PLAYER = StrField('video/player', default='vlc')
    VIDEO_PLAYER.widgetFactory = InitArgWidgetFactory(ComboBoxFieldWidget, 'vlc', 'mpv')


settings = _Settings(orgName, appName)
