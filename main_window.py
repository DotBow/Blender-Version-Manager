import json
import os
import re
import sys
import zipfile
from urllib.request import urlopen
import subprocess
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal

import main_window_design


class YourThreadName(QThread):
    finished = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject')

    def __init__(self, root_path, download_url):
        QThread.__init__(self)
        self.download_url = download_url
        self.root_path = root_path

    def run(self):
        blender_zip = urlopen(self.download_url)
        size = blender_zip.info()['Content-Length']
        download_path = self.root_path + '/' + \
            self.download_url.split('/', -1)[-1]

        with open(download_path, 'wb') as f:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                f.write(chunk)
                self.progress_changed.emit(
                    os.stat(download_path).st_size / int(size))

        zf = zipfile.ZipFile(download_path)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            zf.extract(file, self.root_path)
            extracted_size += file.file_size
            self.progress_changed.emit(extracted_size / uncompress_size)

        self.finished.emit()


class TestButton(QtWidgets.QPushButton):
    def __init__( self, text, parent=None):
        super(TestButton, self).__init__(parent)
        self.setText(text)
        self.clicked.connect(lambda: subprocess.Popen(text + "/blender.exe"))
        #self.clicked.connect(self.deleteLater)


class ExampleApp(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionQuit.triggered.connect(lambda: sys.exit())

        self.btnSetRootFolder.clicked.connect(self.set_root_folder)
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)

        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnCancel.hide()

        root_path = self.read_settings("root_path")
        self.labelRootFolder.setText(
            root_path if root_path else "No Root Folder Specified!")

        dirs = next(os.walk(root_path))[1]
        prog = re.compile("blender-2.80")
        for dir in dirs:
            if prog.match(dir):
                self.test.addWidget(TestButton(root_path + "/" + dir))

    def set_root_folder(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Choose folder")

        if dir:
            self.write_settings("root_path", dir)
            self.labelRootFolder.setText(dir)

    def read_settings(self, key):
        with open("settings.txt", 'r') as settings_file:
            settings_data = json.load(settings_file)
            settings_file.close()

        return settings_data[key]

    def write_settings(self, key, value):
        with open("settings.txt", 'r') as settings_file:
            settings_data = json.load(settings_file)
            settings_file.close()

        settings_data[key] = value

        with open("settings.txt", 'w') as settings_file:
            settings_file.write(json.dumps(settings_data))
            settings_file.close()

    def is_root_folder_settings_enabled(self, is_enabled):
        items = (self.layoutRootFolderSettings.itemAt(i).widget()
                 for i in range(self.layoutRootFolderSettings.count()))
        for w in items:
            w.setEnabled(is_enabled)

    def update(self):
        self.btnUpdate.hide()
        self.btnCancel.show()
        self.is_root_folder_settings_enabled(False)

        self.thread = YourThreadName(
            self.read_settings("root_path"), self.get_url())
        self.thread.finished.connect(self.finished)
        self.thread.progress_changed.connect(self.update_progress_bar)
        self.btnCancel.clicked.connect(self.thread.terminate)
        self.thread.start()

    def finished(self):
        self.btnCancel.hide()
        self.btnUpdate.show()
        self.progressBar.setValue(0)
        self.is_root_folder_settings_enabled(True)

    def cancel(self):
        self.finished()

    def update_progress_bar(self, val):
        self.progressBar.setValue(val * 100)

    def open_root_folder(self):
        root_path = self.read_settings("root_path")

        if root_path:
            os.startfile(root_path)

    # Get download URL from builder page
    def get_url(self):
        builder_url = "https://builder.blender.org"
        builder_content = urlopen(builder_url + "/download").read()
        builder_soup = BeautifulSoup(builder_content, 'html.parser')
        version_url = builder_soup.find(
            href=re.compile("blender-2.80"))['href']
        return builder_url + version_url


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
