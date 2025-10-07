import faulthandler
import logging

from PyQt5.QtWidgets import QApplication

from multi_video import appDisplayName, appName, moduleName, orgName


# noinspection DuplicatedCode
def main():
    faulthandler.enable(all_threads=False)

    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from multi_video.window.main import VideoWindow  # noqa: PLC0415

    app = QApplication([])
    app.setApplicationName(appName)
    app.setOrganizationName(orgName)
    app.setApplicationDisplayName(appDisplayName)

    vw = VideoWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
