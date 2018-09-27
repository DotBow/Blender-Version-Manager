import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QMainWindow,
                             QMessageBox, QPushButton, QSizePolicy)

import main_window_design


class BuildLoader(QThread):
    finished = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, root_path, download_url):
        QThread.__init__(self)
        self.download_url = download_url
        self.root_path = root_path

    def run(self):
        blender_zip = urlopen(self.download_url)
        size = blender_zip.info()['Content-Length']
        temp_path = os.path.join(self.root_path, "temp")

        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        download_path = os.path.join(
            temp_path, self.download_url.split('/', -1)[-1])

        with open(download_path, 'wb') as f:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                f.write(chunk)
                self.progress_changed.emit(
                    os.stat(download_path).st_size / int(size), "Downloading")

        zf = zipfile.ZipFile(download_path)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            zf.extract(file, self.root_path)
            extracted_size += file.file_size
            self.progress_changed.emit(
                extracted_size / uncompress_size, "Extracting")

        self.finished.emit()

    def stop(self):
        self.terminate()
        self.finished.emit()


class B3dVersionItemLayout(QHBoxLayout):
    def __init__(self, path, show_star, parent=None):
        super(B3dVersionItemLayout, self).__init__(parent)
        self.path = path

        self.btnOpen = QPushButton(path)
        self.btnOpen.clicked.connect(
            lambda: subprocess.Popen(path + "/blender.exe"))

        if (show_star):
            self.btnOpen.setIcon(QIcon(os.path.join("icons", "star.png")))

        self.btnDelete = QPushButton("Delete")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.clicked.connect(lambda: self.delete())

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    def delete(self):
        shutil.rmtree(self.path)
        self.parent().parent().parent().parent().draw_versions_layout()


class B3dVersionManger(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join("icons", "blender_logo.png")))

        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionClearTempFolder.triggered.connect(lambda: sys.exit())

        self.btnSetRootFolder.clicked.connect(self.set_root_folder)
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)

        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.hide()

        root_path = self.read_settings("root_path")

        if root_path:
            self.labelRootFolder.setText(root_path)
            self.draw_versions_layout()
        else:
            self.labelRootFolder.setText("No Root Folder Specified!")

    def delete_items(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                self.delete_items(item.layout())

    def collect_versions(self):
        root_path = self.read_settings("root_path")

        if not os.path.exists(root_path):
            os.makedirs(root_path)
            return

        dirs = next(os.walk(root_path))[1]
        prog = re.compile("blender-2.80")

        versions = []

        for dir in dirs:
            if prog.match(dir):
                versions.append(dir)

        return versions

    def draw_versions_layout(self):
        self.delete_items(self.listVersions)
        root_path = self.read_settings("root_path")
        last_verison = self.get_url().split('-',)[-2]

        for dir in self.collect_versions():
            show_star = True if last_verison in dir else False

            self.listVersions.addLayout(
                B3dVersionItemLayout(root_path + "/" + dir, show_star))

    def set_root_folder(self):
        dir = QFileDialog.getExistingDirectory(
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
        last_verison = self.get_url().split('-',)[-2]

        for version in self.collect_versions():
            if last_verison in version:
                QMessageBox.information(
                    self, "Information", "You are up to date!", QMessageBox.Ok)
                return

        self.btnUpdate.hide()
        self.btnCancel.show()
        self.is_root_folder_settings_enabled(False)
        self.thread = BuildLoader(
            self.read_settings("root_path"), self.get_url())
        self.thread.finished.connect(self.finished)
        self.thread.progress_changed.connect(self.update_progress_bar)
        self.btnCancel.clicked.connect(lambda: self.thread.stop())
        self.thread.start()

    def finished(self):
        self.btnCancel.hide()
        self.btnUpdate.show()
        self.progressBar.setValue(0)
        self.is_root_folder_settings_enabled(True)
        self.draw_versions_layout()
        self.labelUpdateStatus.setText("No Tasks")

    def cancel(self):
        self.finished()

    def update_progress_bar(self, val, status):
        self.progressBar.setValue(val * 100)
        self.labelUpdateStatus.setText(status)

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
    window = B3dVersionManger()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
