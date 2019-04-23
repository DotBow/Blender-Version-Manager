import logging
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from main_window import B3dVersionMangerMainWindow

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
    QApplication.setApplicationVersion("1.4.1")

    app = QApplication(sys.argv)
    window = B3dVersionMangerMainWindow(app)
    window.setWindowFlags(Qt.FramelessWindowHint)

    if not window.is_run_minimized:
        window.show()

    app.exec_()


if __name__ == '__main__':
    main()
