import logging
import sys
from time import gmtime, strftime

import psutil
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

    utcnow = strftime(('%Y-%m-%d_%H-%M-%S'), gmtime())
    logging.basicConfig(filename="BVM_Report_" + utcnow +
                        ".log", level=logging.DEBUG)
    logger.error("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OSX',
        'win32': 'Windows'
    }

    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def main():
    raise Exception("x", "x")
    QApplication.setApplicationName("Blender Version Manager")
    QApplication.setApplicationVersion("1.5.1")

    app = QApplication(sys.argv)

    proc_count = len([proc for proc in psutil.process_iter()
                      if proc.name() == "Blender Version Manager.exe"])

    if proc_count > 2:
        msg = QMessageBox(QMessageBox.Warning, "Blender Version Manager",
                          "Another instance is already running!",
                          QMessageBox.Ok)
        msg.setWindowIcon(QIcon(":/icons/app.svg"))
        msg.exec_()
    else:
        window = BVMQMainWindow(app, get_platform())

        if not window.is_run_minimized:
            window.show()

        app.exec_()


if __name__ == '__main__':
    main()
