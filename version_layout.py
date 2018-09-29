import os
import shutil
import subprocess

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QSizePolicy


class B3dVersionItemLayout(QHBoxLayout):
    def __init__(self, root_folder, version, show_star, parent=None):
        super(B3dVersionItemLayout, self).__init__(parent)
        self.path = root_folder
        self.version = version

        self.btnOpen = QPushButton(version)
        self.btnOpen.clicked.connect(
            lambda: subprocess.Popen(os.path.join(root_folder, version, "blender.exe")))

        if (show_star):
            self.btnOpen.setIcon(QIcon(os.path.join("icons", "star.ico")))

        self.btnDelete = QPushButton("Delete")
        self.btnDelete.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.btnDelete.clicked.connect(lambda: self.delete())

        self.addWidget(self.btnOpen)
        self.addWidget(self.btnDelete)

    def delete(self):
        parent = self.parent().parent().parent().parent()

        delete = QMessageBox.question(
            parent, "Warning", "Are you sure you want to delete '" + self.version + "' from disk?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if delete == QMessageBox.Yes:
            shutil.rmtree(self.path)
            parent.draw_versions_layout()
