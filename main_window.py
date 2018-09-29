import json
import os
import re
import shutil
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QLabel, QMainWindow, QMessageBox

import main_window_design
from build_loader import BuildLoader
from version_layout import B3dVersionItemLayout


class B3dVersionMangerMainWindow(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join("icons", "app.ico")))

        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionClearTempFolder.triggered.connect(self.clear_temp_folder)

        self.btnSetRootFolder.clicked.connect(
            lambda: self.set_root_folder(False))
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)

        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.hide()

        self.settings = QSettings('b3d_version_manager', 'settings')
        self.root_folder = self.settings.value('root_folder')

        if (not self.root_folder) or (not os.path.isdir(self.root_folder)):
            self.settings.setValue(
                'root_folder', os.path.dirname(os.path.realpath(__file__)))

        self.root_folder = self.settings.value('root_folder')

        self.labelRootFolder.setText(self.root_folder)
        self.draw_versions_layout()

    def clear_temp_folder(self):
        temp_folder = os.path.join(self.root_folder, "temp")

        if os.path.isdir(temp_folder):
            shutil.rmtree(temp_folder)

    def delete_items(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                self.delete_items(item.layout())

    def collect_versions(self):
        dirs = next(os.walk(self.root_folder))[1]
        prog = re.compile("blender-2.80")

        versions = []

        for dir in dirs:
            if prog.match(dir):
                versions.append(dir)

        return versions

    def draw_versions_layout(self):
        self.delete_items(self.listVersions)
        last_verison = self.get_url().split('-',)[-2]
        versions = self.collect_versions()

        if versions:
            for version in versions:
                show_star = True if last_verison in version else False

                self.listVersions.addLayout(
                    B3dVersionItemLayout(self.root_folder, version, show_star))
        else:
            self.listVersions.addWidget(QLabel("No Versions Found!"))

    def set_root_folder(self, warning):
        dir = QFileDialog.getExistingDirectory(
            self, "Choose Root Folder")

        if dir:
            self.settings.setValue('root_folder', dir)
            self.labelRootFolder.setText(dir)
            self.draw_versions_layout()

    def is_root_folder_settings_enabled(self, is_enabled):
        items = (self.layoutRootFolderSettings.itemAt(i).widget()
                 for i in range(self.layoutRootFolderSettings.count()))

        for item in items:
            item.setEnabled(is_enabled)

    def update(self):
        last_verison = self.get_url().split('-',)[-2]
        versions = self.collect_versions()

        if versions:
            for version in versions:
                if last_verison in version:
                    QMessageBox.information(
                        self, "Information", "You are up to date!", QMessageBox.Ok)
                    return

        self.btnUpdate.hide()
        self.btnCancel.show()
        self.is_root_folder_settings_enabled(False)
        self.thread = BuildLoader(
            self.root_folder, self.get_url())
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
        os.startfile(self.root_folder)

    def get_url(self):
        builder_url = "https://builder.blender.org"
        builder_content = urlopen(builder_url + "/download").read()
        builder_soup = BeautifulSoup(builder_content, 'html.parser')
        version_url = builder_soup.find(
            href=re.compile("blender-2.80"))['href']
        return builder_url + version_url
