import asyncio
import os
import shutil
import subprocess
import threading
import time

import psutil
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMessageBox,
                             QPushButton, QSizePolicy)

import resources_rc


class B3dItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, is_latest, parent):
        super(B3dItemLayout, self).__init__(None)
        self.btn_open_style = \
            ("""QPushButton
                    {
                        color: rgb(255, 255, 255);
                        background-color: rgb(51, 51, 51);
                        border-style: solid;
                        border-color: rgb(51, 51, 51);
                        border-width: 6px;
                    }

                    QPushButton:pressed
                    {
                        background-color: rgb(80, 80, 80);
                        border-color: rgb(80, 80, 80);
                    }

                    QPushButton:hover
                    {
                        background-color: rgb(80, 80, 80);
                        border-color: rgb(80, 80, 80);
                    }""")

        self.btn_delete_style = \
            ("""QPushButton
                    {
                        color: rgb(255, 255, 255);
                        background-color: rgb(51, 51, 51);
                        border-style: solid;
                        border-color: rgb(51, 51, 51);
                        border-width: 0px 4px 0px 4px;
                        qproperty-icon: url(:/icons/delete.svg);
                        qproperty-iconSize: 20px;
                    }

                    QPushButton:pressed
                    {
                        background-color: rgb(80, 80, 80);
                        border-color: rgb(80, 80, 80);
                    }

                    QPushButton:hover
                    {
                        background-color: rgb(80, 80, 80);
                        border-color: rgb(80, 80, 80);
                    }""")

        self.btn_open_running_style = \
            ("""QPushButton
                    {
                        color: rgb(255, 255, 255);
                        background-color: rgb(204, 102, 51);
                        border-style: solid;
                        border-color: rgb(204, 102, 51);
                        border-width: 6px;
                    }

                    QPushButton:pressed
                    {
                        background-color: rgb(204, 102, 51);
                        border-color: rgb(204, 102, 51);
                    }

                    QPushButton:hover
                    {
                        background-color: rgb(204, 102, 51);
                        border-color: rgb(204, 102, 51);
                    }""")

        self.btn_delete_running_style = \
            ("""QPushButton
                    {
                        color: rgb(255, 255, 255);
                        background-color: rgb(0, 122, 204);
                        border-style: solid;
                        border-color: rgb(0, 122, 204);
                        border-width: 0px 13px 0px 13px;
                        qproperty-icon: none;
                    }

                    QPushButton:hover
                    {
                        background-color: rgb(80, 80, 80);
                        border-color: rgb(80, 80, 80);
                    }""")

        self.pids = []
        self.root_folder = root_folder
        self.version = version
        self.parent = parent

        self.setContentsMargins(6, 0, 6, 0)
        self.setSpacing(0)

        ctime = os.path.getctime(os.path.join(
            root_folder, version, "blender.exe"))
        fctime = time.strftime("%d-%b-%Y", time.gmtime(ctime))

        self.btnOpen = QPushButton(
            (version.split('-',)[-2]).replace("git.", "Git-") + " | " + fctime)
        self.btnOpen.clicked.connect(self.open)

        if (is_latest):
            self.btnOpen.setIcon(parent.star_icon)
            self.parent.blender_action.triggered.disconnect()
            self.parent.blender_action.triggered.connect(self.open)
        else:
            self.btnOpen.setIcon(parent.fake_icon)

        self.btnOpen.setFont(QFont("MS Shell Dlg 2", 10))
        self.btnDelete = QPushButton("")
        self.btnDelete.setStyleSheet(self.btn_delete_style)
        self.btnOpen.setStyleSheet(self.btn_open_style)
        self.btnDelete.setFlat(True)
        self.btnDelete.setToolTip("Delete From Drive")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnOpen.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDelete.clicked.connect(lambda: self.delete())

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    async def wait_for_exit(self):
        loop = asyncio.get_running_loop()

        while True:
            for pid in self.pids:
                if not psutil.pid_exists(pid):
                    self.pids.remove(pid)
                    self.btnDelete.setText(str(len(self.pids)))

                    if len(self.pids) == 0:
                        self.btnOpen.setStyleSheet(self.btn_open_style)
                        self.btnOpen.setEnabled(True)

                        self.btnDelete.setStyleSheet(self.btn_delete_style)
                        self.btnDelete.setIcon(self.parent.trash_icon)
                        self.btnDelete.setText("")
                        self.btnDelete.setToolTip("Delete From Drive")
                        self.btnDelete.setEnabled(True)

                        break

            await asyncio.sleep(1)

    def open(self):
        proc = subprocess.Popen(os.path.join(
            self.root_folder, self.version, "blender.exe"))
        self.pids.append(proc.pid)
        self.btnDelete.setText(str(len(self.pids)))

        if len(self.pids) == 1:
            self.btnOpen.setStyleSheet(self.btn_open_running_style)
            self.btnDelete.setToolTip("Number of Running Instances")
            self.btnDelete.setStyleSheet(self.btn_delete_running_style)
            self.btnDelete.setEnabled(False)

            threading.Thread(target=lambda: asyncio.run(
                self.wait_for_exit()), daemon=True).start()

    def delete(self):
        delete = QMessageBox.warning(
            self.parent,
            "Warning",
            "Are you sure you want to delete\n'" + self.btnOpen.text() + "'\nfrom drive?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if delete == QMessageBox.Yes:
            threading.Thread(target=lambda: asyncio.run(
                self.delete_tread())).start()

    async def delete_tread(self):
        self.btnOpen.setText("Deleting...")
        self.btnOpen.setEnabled(False)
        self.btnDelete.hide()
        shutil.rmtree(os.path.join(self.root_folder, self.version))
        self.parent.cleanup_layout(self.layout())
