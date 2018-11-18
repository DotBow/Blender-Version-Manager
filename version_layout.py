import os
import shutil
import subprocess
import time

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont, QCursor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMessageBox,
                             QPushButton, QSizePolicy)

import resources_rc


class B3dItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, is_latest, parent):
        super(B3dItemLayout, self).__init__(None)
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
        self.btnOpen.clicked.connect(
            lambda: subprocess.Popen(os.path.join(root_folder, version, "blender.exe")))

        if (is_latest):
            self.btnOpen.setIcon(parent.star_icon)
        else:
            self.btnOpen.setIcon(parent.fake_icon)

        self.btnOpen.setFont(QFont("MS Shell Dlg 2", 10))

        btn_open_style = \
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
        btn_delete_style = \
                ("""QPushButton
                 {
                     color: rgb(255, 255, 255);
                     background-color: rgb(51, 51, 51);
                     border-style: solid;
                     border-color: rgb(51, 51, 51);
                     border-width: 0px 4px 0px 4px;
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
        self.btnDelete = QPushButton(parent.trash_icon, "")
        self.btnDelete.setStyleSheet(btn_delete_style)
        self.btnOpen.setStyleSheet(btn_open_style)
        self.btnDelete.setIconSize(QtCore.QSize(20, 20))
        self.btnDelete.setFlat(True)
        self.btnDelete.setToolTip("Delete From Drive")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnOpen.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.btnDelete.clicked.connect(lambda: self.delete())

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    def delete(self):
        delete = QMessageBox.warning(
            self.parent,
            "Warning",
            "Are you sure you want to delete\n'" + self.btnOpen.text() + "'\nfrom drive?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if delete == QMessageBox.Yes:
            self.btnOpen.setText("Deleting...")
            self.btnOpen.setEnabled(False)
            self.btnDelete.setEnabled(False)
            QApplication.processEvents()
            shutil.rmtree(os.path.join(self.root_folder, self.version))
            self.parent.draw_list_versions()
