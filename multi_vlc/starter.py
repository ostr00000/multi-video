import logging

from multi_vlc import moduleName, appName


def main():
    logging.basicConfig(level=logging.DEBUG)
    mainLogger = logging.getLogger(moduleName)
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication
    from multi_vlc.vlc_window import VlcWindow

    app = QApplication([])
    app.setApplicationName(appName)

    vw = VlcWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
