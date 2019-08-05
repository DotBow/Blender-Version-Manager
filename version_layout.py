import asyncio
import os
import re
import shutil
import subprocess
import threading
import time
from subprocess import DEVNULL

import psutil
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QSizePolicy

from _platform import get_platform

if get_platform() == 'Windows':
    from subprocess import CREATE_NO_WINDOW


class B3dItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, is_latest, parent):
        super(B3dItemLayout, self).__init__(None)
        self.is_latest = is_latest

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
                    background-color: rgb(223, 121, 70);
                    border-color: rgb(223, 121, 70);
                }

                QPushButton[IsRunning=true]:hover
                {
                    background-color: rgb(223, 121, 70);
                    border-color: rgb(223, 121, 70);
                }""")

        self.btn_delete_style = \
            ("""QPushButton[IsRunning=false]
                {
                    color: rgb(255, 255, 255);
                    background-color: rgb(51, 51, 51);
                    border-style: solid;
                    border-color: rgb(51, 51, 51);
                    border-width: 0px 4px 0px 4px;
                    qproperty-icon: url(:/icons/delete.png);
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

        self.platform = get_platform()

        if self.platform == 'Windows':
            blender_exe = "blender.exe"
        elif self.platform == 'Linux':
            blender_exe = "blender"

        self.parent = parent
        self.root_folder = root_folder
        self.version = version
        self.pids = []
        self.mtime = os.path.getmtime(os.path.join(
            root_folder, version, blender_exe))

        self.setContentsMargins(6, 0, 6, 0)
        self.setSpacing(0)

        b3d_exe = os.path.join(root_folder, version, blender_exe)

        if self.platform == 'Windows':
            info = subprocess.check_output(
                [b3d_exe, "-v"], creationflags=CREATE_NO_WINDOW, shell=True,
                stderr=DEVNULL, stdin=DEVNULL).decode('UTF-8')
        elif self.platform == 'Linux':
            info = subprocess.check_output(
                [b3d_exe, "-v"], shell=False,
                stderr=DEVNULL, stdin=DEVNULL).decode('UTF-8')

        ctime = re.search("build commit time: " + "(.*)", info)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", info)[1].rstrip()
        self.git = re.search("build hash: " + "(.*)", info)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")

        self.btnOpen = QPushButton(
            "Git-%s | %s" % (self.git, time.strftime("%d-%b-%H:%M", strptime)))
        self.btnOpen.clicked.connect(self.open)

        self.set_is_latest(self.is_latest)

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
        self.is_latest = is_latest

        if self.is_latest:
            self.btnOpen.setIcon(self.parent.icon_star)
        else:
            self.btnOpen.setIcon(self.parent.icon_fake)

    def open(self):
        if self.platform == 'Windows':
            DETACHED_PROCESS = 0x00000008
            b3d_exe = os.path.join(
                self.root_folder, self.version, "blender.exe")
            process = subprocess.Popen(b3d_exe, shell=True, stdin=None, stdout=None,
                                       stderr=None, close_fds=True, creationflags=DETACHED_PROCESS)
        elif self.platform == 'Linux':
            b3d_exe = os.path.join(self.root_folder, self.version, "blender")
            process = subprocess.Popen(b3d_exe, shell=True, stdin=None, stdout=None,
                                       stderr=None, close_fds=True)

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
        self.btnDelete.setIcon(self.parent.icon_trash)
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
        if self.is_latest:
            self.set_is_latest(False)

            if (not self.parent.is_update_running and not self.parent.progressBar.isVisible()):
                self.parent.stop_uptodate_thread()
                self.parent.start_uptodate_thread()

            if len(self.parent.layouts) > 1:
                self.parent.layouts[1].set_is_latest(True)

        self.btnOpen.setText("Deleting...")
        self.btnOpen.setEnabled(False)
        self.btnDelete.setIcon(self.parent.icon_fake)
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
