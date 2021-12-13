from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog

from multi_video import orgName, appName
from pyqt_settings.factory.base import WidgetFactory, ConfigFunc
from pyqt_settings.field.control import ControlledField
from pyqt_settings.field.list import ListField
from pyqt_settings.field.simple import StrField, PathField, IntField, BoolField
from pyqt_settings.gui_widget.path_line_edit import PathLineEdit
from pyqt_settings.gui_widget.simple import ComboBoxFieldWidget


class _Settings(QSettings):
    LAST_PATH = StrField('lastConfig/path')
    ASK_TO_SAVE_CHANGED_DATA = BoolField('ask/unsaved', default=True)
    ALLOWED_EXTENSIONS = ListField('load/allowedExtensions', default=('mp4', 'webm', 'avi'))
    DRAG_MULTIPLE_CREATE_ONE = BoolField('load/dragMultipleCreateOne', default=True)
    DRAG_CREATE_RECURSIVE = BoolField('load/dragCreateRecursive', default=True)

    @property
    def allowedExtensionsWithDot(self) -> list[str]:
        return ['.' + ae for ae in videoSettings.ALLOWED_EXTENSIONS]

    VIDEO_PLAYER = StrField('video/player', default='vlc')
    VIDEO_PLAYER.widgetFactory = WidgetFactory(ComboBoxFieldWidget, 'vlc', 'mpv')

    SHUFFLE_INTERNAL_ORDER = BoolField('shuffle/internal', default=True)

    IS_RANDOM_PART_ACTIVE = BoolField('video/randomPart', default=True)
    MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART = IntField('video/minimal_length', default=120)
    RANDOM_PART_DURATION = IntField('video/duration', default=60)

    _MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART_LLsJJ = ControlledField(
        IS_RANDOM_PART_ACTIVE, MINIMAL_LENGTH_TO_ACTIVATE_RANDOM_PART)
    _RANDOM_PART_DURATION_LLsJJ = ControlledField(
        IS_RANDOM_PART_ACTIVE, RANDOM_PART_DURATION)

    VLC_SLEEP_TIME_LLmsJJ = IntField('vlc/sleepTime', default=1000)

    TAG_DIR = PathField('AddFromTag/tagDir')
    TAG_DIR.widgetFactory = WidgetFactory(
        PathLineEdit, configFunctions=[
            ConfigFunc(QFileDialog.setFileMode, QFileDialog.Directory),
            ConfigFunc(QFileDialog.setWindowTitle, "Select tag directory")]
    )
    TAG_CACHE = ListField('AddFromTag/cache', castType=str)

    TAG_DEFAULT_ACTION = StrField('AddFromTag/defaultAction')


videoSettings = _Settings(orgName, appName)
