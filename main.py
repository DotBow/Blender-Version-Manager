import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from main_window import B3dVersionMangerMainWindow


def main():
    QApplication.setApplicationName("Blender Version Manager")
    QApplication.setApplicationVersion("1.3.0")

    app = QApplication(sys.argv)
    window = B3dVersionMangerMainWindow(app)
    window.setWindowFlags(Qt.FramelessWindowHint)

    if not window.is_run_minimized:
        window.show()

    app.exec_()


if __name__ == '__main__':
    main()
