import json
import os
import sys
from threading import Thread

from PyQt5 import QtWidgets

import build_manager as build_mng
import main_window_design


class ExampleApp(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionSetRootFolder.triggered.connect(self.browse_folder)
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)
        self.btnCancel.hide()

        root_path = self.read_settings('root_path')
        self.labelRootPath.setText(
            root_path if root_path else "No Root Folder Specified!")

    def browse_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Выберите папку")

        if dir:
            self.write_settings('root_path', dir)
            self.labelRootPath.setText(dir)

    def read_settings(self, key):
        with open('settings.txt', 'r') as settings_file:
            settings_data = json.load(settings_file)
            settings_file.close()

        return settings_data[key]

    def write_settings(self, key, value):
        with open('settings.txt', 'r') as settings_file:
            settings_data = json.load(settings_file)
            settings_file.close()

        settings_data[key] = value

        with open('settings.txt', 'w') as settings_file:
            settings_file.write(json.dumps(settings_data))
            settings_file.close()

    def update(self):
        root_path = self.read_settings('root_path')
        self.btnUpdate.hide()
        self.btnCancel.show()
        self.t = Thread(target = build_mng.load_zip(self.progressBar, root_path))

        self.btnCancel.hide()
        self.btnUpdate.show()

    def cancel(self):
        self.t._stop()

    def open_root_folder(self):
        root_path = self.read_settings('root_path')

        if root_path:
            os.startfile(root_path)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
