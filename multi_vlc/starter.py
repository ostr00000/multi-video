import logging


def main():
    logging.basicConfig()
    mainLogger = logging.getLogger('multi_vlc')
    mainLogger.setLevel(logging.DEBUG)

    from PyQt5.QtWidgets import QApplication
    from multi_vlc.vlc_window import VlcWindow

    app = QApplication([])
    vw = VlcWindow()
    vw.show()
    app.exec()


if __name__ == '__main__':
    main()
