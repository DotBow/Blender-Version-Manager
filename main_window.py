import json
import sys

from PyQt5 import QtWidgets

import main_window_design
import build_manager as build_mng


class ExampleApp(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionSetRootFolder.triggered.connect(self.browse_folder)
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.hide()

    def browse_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")

        if dir:
            self.write_settings('root_folder', dir)

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
        build_mng.load_zip(self.progressBar, root_path)
        self.btnUpdate.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
