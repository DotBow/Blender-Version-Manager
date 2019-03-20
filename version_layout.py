import asyncio
import os
import re
import shutil
import subprocess
import threading
import time
from subprocess import CREATE_NO_WINDOW

import psutil
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QSizePolicy


class B3dItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, is_latest, parent):
        super(B3dItemLayout, self).__init__(None)

        self.btn_open_style = \
            ("""QPushButton[IsRunning=false]
                {
                    color: rgb(255, 255, 255);
                    background-color: rgb(51, 51, 51);
                    border-style: solid;
                    border-color: rgb(51, 51, 51);
                    border-width: 6px;
                }

                QPushButton[IsRunning=false]:pressed
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }

                QPushButton[IsRunning=false]:hover
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }

                QPushButton[IsRunning=true]
                {
                    color: rgb(255, 255, 255);
                    background-color: rgb(204, 102, 51);
                    border-style: solid;
                    border-color: rgb(204, 102, 51);
                    border-width: 6px;
                }

                QPushButton[IsRunning=true]:pressed
                {
                    background-color: rgb(204, 102, 51);
                    border-color: rgb(204, 102, 51);
                }

                QPushButton[IsRunning=true]:hover
                {
                    background-color: rgb(204, 102, 51);
                    border-color: rgb(204, 102, 51);
                }""")

        self.btn_delete_style = \
            ("""QPushButton[IsRunning=false]
                {
                    color: rgb(255, 255, 255);
                    background-color: rgb(51, 51, 51);
                    border-style: solid;
                    border-color: rgb(51, 51, 51);
                    border-width: 0px 4px 0px 4px;
                    qproperty-icon: url(:/icons/delete.svg);
                    qproperty-iconSize: 20px;
                }

                QPushButton[IsRunning=false]:pressed
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }

                QPushButton[IsRunning=false]:hover
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }

                QPushButton[IsRunning=true]
                {
                    color: rgb(255, 255, 255);
                    background-color: rgb(0, 122, 204);
                    border-style: solid;
                    border-color: rgb(0, 122, 204);
                    border-width: 0px 13px 0px 13px;
                    qproperty-icon: none;
                }

                QPushButton[IsRunning=true]:pressed
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }

                QPushButton[IsRunning=true]:hover
                {
                    background-color: rgb(80, 80, 80);
                    border-color: rgb(80, 80, 80);
                }""")

        self.parent = parent
        self.root_folder = root_folder
        self.version = version
        self.pids = []
        self.mtime = os.path.getmtime(os.path.join(root_folder, version, "blender.exe"))

        self.setContentsMargins(6, 0, 6, 0)
        self.setSpacing(0)

        b3d_exe = os.path.join(root_folder, version, "blender.exe")
        info = subprocess.check_output(
            [b3d_exe, "-v"], creationflags=CREATE_NO_WINDOW).decode('UTF-8')

        ctime = re.search("build commit time: " + "(.*)", info)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", info)[1].rstrip()
        git = re.search("build hash: " + "(.*)", info)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")

        self.btnOpen = QPushButton(
            "Git-%s | %s" % (git, time.strftime("%d-%b-%H:%M", strptime)))
        self.btnOpen.clicked.connect(self.open)

        self.set_is_latest(is_latest)
        self.parent.blender_action.triggered.disconnect()
        self.parent.blender_action.triggered.connect(self.open)

        self.btnOpen.setFont(QFont("MS Shell Dlg 2", 10))
        self.btnOpen.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnOpen.setStyleSheet(self.btn_open_style)
        self.btnOpen.setProperty('IsRunning', False)

        self.btnDelete = QPushButton("")
        self.btnDelete.setFlat(True)
        self.btnDelete.setToolTip("Delete From Drive")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnDelete.clicked.connect(lambda: self.delete())
        self.btnDelete.setStyleSheet(self.btn_delete_style)
        self.btnDelete.setProperty('IsRunning', False)

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    def set_is_latest(self, is_latest):
        if is_latest:
            self.btnOpen.setIcon(self.parent.star_icon)
        else:
            self.btnOpen.setIcon(self.parent.fake_icon)

    def open(self):
        process = subprocess.Popen(os.path.join(
            self.root_folder, self.version, "blender.exe"))
        self.pids.append(process.pid)

        if (len(self.pids) == 1):
            self.observe_instances = ObserveInstances(self)
            self.observe_instances.started.connect(self.observe_started)
            self.observe_instances.finished.connect(self.observe_finished)
            self.observe_instances.count_changed.connect(self.count_changed)
            self.observe_instances.start()
        else:
            self.count_changed()

    def observe_started(self):
        self.count_changed()
        self.btnOpen.setProperty('IsRunning', True)
        self.btnOpen.setStyle(self.btnOpen.style())
        self.btnDelete.setToolTip("Number of Running Instances")
        self.btnDelete.setProperty('IsRunning', True)
        self.btnDelete.setStyle(self.btnDelete.style())
        self.btnDelete.setEnabled(False)

    def observe_finished(self):
        self.btnOpen.setProperty('IsRunning', False)
        self.btnOpen.setStyle(self.btnOpen.style())
        self.btnDelete.setIcon(self.parent.trash_icon)
        self.btnDelete.setText("")
        self.btnDelete.setToolTip("Delete From Drive")
        self.btnDelete.setEnabled(True)
        self.btnDelete.setProperty('IsRunning', False)
        self.btnDelete.setStyle(self.btnDelete.style())

    def count_changed(self):
        self.btnDelete.setText(str(len(self.pids)))

    def delete(self):
        msgBox = QMessageBox.question(
            self.parent, "Blender Version Manager",
            "Are you sure you want to delete\n'" + self.btnOpen.text() + "'?",
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)

        if msgBox == QMessageBox.Yes:
            threading.Thread(target=lambda: asyncio.run(
                self.delete_tread())).start()

    async def delete_tread(self):
        self.set_is_latest(False)
        self.btnOpen.setText("Deleting...")
        self.btnOpen.setEnabled(False)
        self.btnDelete.hide()
        shutil.rmtree(os.path.join(self.root_folder, self.version))
        self.parent.layouts.remove(self)
        self.parent.cleanup_layout(self.layout())


class ObserveInstances(QThread):
    started = pyqtSignal()
    finished = pyqtSignal()
    count_changed = pyqtSignal()

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent

    def run(self):
        self.started.emit()

        while self.parent:
            for pid in self.parent.pids:
                if not psutil.pid_exists(pid):
                    self.parent.pids.remove(pid)

                if len(self.parent.pids) > 0:
                    self.count_changed.emit()
                else:
                    self.finished.emit()
                    return

            QThread.sleep(1)
