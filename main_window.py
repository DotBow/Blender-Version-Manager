import json
import os
import re
import shutil
import subprocess
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QFileDialog, QLabel, QMainWindow, QMenu,
                             QMessageBox, QSystemTrayIcon)

import main_window_design
from build_loader import BuildLoader
from version_layout import B3dVersionItemLayout


class B3dVersionMangerMainWindow(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join("icons", "app.ico")))

        self.settings = QSettings('b3d_version_manager', 'settings')
        root_folder = self.settings.value('root_folder')

        if (not root_folder) or (not os.path.isdir(root_folder)):
            self.settings.setValue(
                'root_folder', os.path.dirname(os.path.realpath(__file__)))

        self.actionClearTempFolder.triggered.connect(self.clear_temp_folder)
        self.actionMinimizeToTray.setChecked(
            self.settings.value('minimize_to_tray', type=bool))
        self.actionMinimizeToTray.triggered.connect(self.minimize_to_tray)
        self.actionQuit.triggered.connect(self.quit)

        self.btnSetRootFolder.clicked.connect(self.set_root_folder)
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)

        self.btnUpdate.clicked.connect(self.update)
        self.btnCancel.clicked.connect(self.cancel_thread)
        self.btnCancel.hide()

        self.labelRootFolder.setText(self.settings.value('root_folder'))
        self.is_thread_running = False

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join("icons", "app.ico")))

        self.blender_action = QAction("Blender", self)
        self.blender_action.setIcon(QIcon(os.path.join("icons", "star.ico")))
        self.blender_action.setVisible(False)
        show_action = QAction("Show", self)
        quit_action = QAction("Quit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.blender_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(hide_action)
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.draw_versions_layout()

    def quit(self):
        if self.can_quit():
            self.app.quit()

    def can_quit(self):
        if self.is_thread_running:
            QMessageBox.information(
                self, "Warning", "Update task in progress!", QMessageBox.Ok)
            return False
        else:
            return True

    def minimize_to_tray(self, is_checked):
        self.settings.setValue('minimize_to_tray', is_checked)

    def clear_temp_folder(self):
        if not self.can_quit():
            return

        temp_folder = os.path.join(self.settings.value('root_folder'), "temp")

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
        dirs = next(os.walk(self.settings.value('root_folder')))[1]
        prog = re.compile("blender-2.80")

        versions = []

        for dir in dirs:
            if prog.match(dir):
                versions.append(dir)

        return versions

    def draw_versions_layout(self):
        self.delete_items(self.listVersions)
        root_folder = self.settings.value('root_folder')
        versions = self.collect_versions()

        if versions:
            latest_ver = ""
            latest_time = 0

            for ver in versions:
                time = os.path.getctime(os.path.join(
                    root_folder, ver, "blender.exe"))
                if time > latest_time:
                    latest_time = time
                    latest_ver = ver

            for ver in versions:
                is_latest = True if ver == latest_ver else False
                b3d_item_layout = B3dVersionItemLayout(
                    root_folder, ver, is_latest)
                self.listVersions.addLayout(b3d_item_layout)

                if is_latest:
                    self.blender_action.triggered.connect(
                        lambda: subprocess.Popen(os.path.join(root_folder, ver, "blender.exe")))
                    self.blender_action.setVisible(True)
        else:
            self.listVersions.addWidget(QLabel("No Versions Found!"))

    def set_root_folder(self):
        dir = QFileDialog.getExistingDirectory(
            self, "Choose Root Folder", self.settings.value('root_folder'))

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

        self.thread = QThread()
        self.build_loader = BuildLoader(
            self.settings.value('root_folder'), self.get_url())
        self.build_loader.moveToThread(self.thread)
        self.build_loader.finished.connect(self.finished)
        self.build_loader.progress_changed.connect(self.update_progress_bar)
        self.thread.started.connect(self.build_loader.run)
        self.is_thread_running = True
        self.thread.start()

    def cancel_thread(self):
        self.thread.terminate()
        self.build_loader.stop()

    def finished(self):
        self.btnCancel.hide()
        self.btnUpdate.show()
        self.is_root_folder_settings_enabled(True)
        self.update_progress_bar(0, "No Tasks")
        self.draw_versions_layout()
        self.is_thread_running = False
        self.tray_icon.showMessage(
            "Blender Version Manager", "Update finished!", QSystemTrayIcon.Information, 2000)

    def update_progress_bar(self, val, status):
        self.progressBar.setValue(val * 100)
        self.labelUpdateStatus.setText(status)

    def open_root_folder(self):
        os.startfile(self.settings.value('root_folder'))

    def get_url(self):
        builder_url = "https://builder.blender.org"
        builder_content = urlopen(builder_url + "/download").read()
        builder_soup = BeautifulSoup(builder_content, 'html.parser')
        version_url = builder_soup.find(
            href=re.compile("blender-2.80"))['href']
        return builder_url + version_url

    def closeEvent(self, event):
        if self.actionMinimizeToTray.isChecked():
            event.ignore()
            self.hide()
        elif not self.can_quit():
            event.ignore()
        else:
            event.accept()
