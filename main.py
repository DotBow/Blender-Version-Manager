import sys

from PyQt5 import QtWidgets

from main_window import B3dVersionMangerMainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = B3dVersionMangerMainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
