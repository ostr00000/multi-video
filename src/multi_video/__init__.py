from pathlib import Path

from PyQt5.QtCore import QDir

modulePath = Path(__file__).resolve().parent
moduleName = __name__
appName = "multi-video"
appDisplayName = "Multi Video"
orgName = 'ostr00000'

resourcePath = modulePath / "resources"
if not resourcePath.exists():
    _msg = "Cannot find resources directory"
    raise FileNotFoundError(_msg)

QDir.addSearchPath(appName, str(resourcePath))
