import os
from pathlib import Path

from PyQt5.QtCore import QDir

moduleName = os.path.dirname(os.path.abspath(__name__))
appName = "multi-video"
appDisplayName = "Multi Video"
orgName = 'ostr00000'

resourcePath = Path(__file__).resolve().parent / 'resources'
assert resourcePath.exists()
QDir.addSearchPath(appName, str(resourcePath))
