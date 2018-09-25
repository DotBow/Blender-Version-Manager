# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repositories\Blender-Version-Manager\main_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(516, 339)
        MainWindow.setAccessibleDescription("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelRootPath = QtWidgets.QLabel(self.centralwidget)
        self.labelRootPath.setObjectName("labelRootPath")
        self.horizontalLayout_2.addWidget(self.labelRootPath)
        self.btnOpenRootFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenRootFolder.setObjectName("btnOpenRootFolder")
        self.horizontalLayout_2.addWidget(self.btnOpenRootFolder)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelUpdateStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelUpdateStatus.setObjectName("labelUpdateStatus")
        self.horizontalLayout.addWidget(self.labelUpdateStatus)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setObjectName("btnUpdate")
        self.horizontalLayout.addWidget(self.btnUpdate)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 516, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSetRootFolder = QtWidgets.QAction(MainWindow)
        self.actionSetRootFolder.setObjectName("actionSetRootFolder")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionSetRootFolder)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blender Version Manager"))
        self.labelRootPath.setText(_translate("MainWindow", "No root folder specified!"))
        self.btnOpenRootFolder.setText(_translate("MainWindow", "Open"))
        self.labelUpdateStatus.setText(_translate("MainWindow", "Downloading"))
        self.btnUpdate.setText(_translate("MainWindow", "Update"))
        self.btnCancel.setText(_translate("MainWindow", "Cancel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSetRootFolder.setText(_translate("MainWindow", "Set Root Folder"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

