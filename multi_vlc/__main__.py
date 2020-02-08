import logging

from multi_vlc import moduleName, appName, appDisplayName


def main():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication
    from multi_vlc.vlc_window.main import VlcWindow

    app = QApplication([])
    app.setApplicationName(appName)
    app.setApplicationDisplayName(appDisplayName)

    vw = VlcWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
