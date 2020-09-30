from PyQt5.QtCore import QSettings

from multi_video import orgName, appName
from pyqt_settings.factory.base import InitArgWidgetFactory
from pyqt_settings.field.boolean import BoolField
from pyqt_settings.field.control import ControlledField
from pyqt_settings.field.integer import IntField
from pyqt_settings.field.list import ListField
from pyqt_settings.field.string import StrField
from pyqt_settings.gui_widget.combo_box import ComboBoxFieldWidget


class _Settings(QSettings):
    LAST_PATH = StrField('lastConfig/path')
    ASK_TO_SAVE_CHANGED_DATA = BoolField('ask/unsaved', default=True)
    ALLOWED_EXTENSIONS = ListField('extensions/allowed', default=('mp4', 'webm', 'avi'))

    VIDEO_PLAYER = StrField('video/player', default='vlc')
    VIDEO_PLAYER.widgetFactory = InitArgWidgetFactory(ComboBoxFieldWidget, 'vlc', 'mpv')

    SHUFFLE_INTERNAL_ORDER = BoolField('shuffle/internal', default=True)

    IS_RANDOM_PART_ACTIVE = BoolField('video/randomPart', default=True)
    MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART = IntField('video/minimal_length', default=120)
    RANDOM_PART_DURATION = IntField('video/duration', default=60)

    _MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART_LLsJJ = ControlledField(
        IS_RANDOM_PART_ACTIVE, MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART)
    _RANDOM_PART_DURATION_LLsJJ = ControlledField(
        IS_RANDOM_PART_ACTIVE, RANDOM_PART_DURATION)

    VLC_SLEEP_TIME_LLmsJJ = IntField('vlc/sleepTime', default=1000)


videoSettings = _Settings(orgName, appName)
