import logging
import sys

import psutil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from main_window import BVMQMainWindow

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.basicConfig(filename="b3d_version_manager.log",
                        level=logging.DEBUG)
    logger.error("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def main():
    QApplication.setApplicationName("Blender Version Manager")
    QApplication.setApplicationVersion("1.5.1")

    app = QApplication(sys.argv)

    proc_count = len([proc for proc in psutil.process_iter()
                      if proc.name() == "Blender Version Manager.exe"])

    if proc_count > 2:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowIcon(QIcon(":/icons/app.svg"))
        msg.setText(
            "One instance of Blender Version Manager \nis already running!")
        msg.setWindowTitle("Blender Version Manager")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    else:
        window = BVMQMainWindow(app)
        window.setWindowFlags(Qt.FramelessWindowHint)

        if not window.is_run_minimized:
            window.show()

        app.exec_()


if __name__ == '__main__':
    main()
