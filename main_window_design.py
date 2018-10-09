# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_design.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAccessibleDescription("")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutRootFolderSettings = QtWidgets.QHBoxLayout()
        self.layoutRootFolderSettings.setObjectName("layoutRootFolderSettings")
        self.labelRootFolder = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRootFolder.sizePolicy().hasHeightForWidth())
        self.labelRootFolder.setSizePolicy(sizePolicy)
        self.labelRootFolder.setObjectName("labelRootFolder")
        self.layoutRootFolderSettings.addWidget(self.labelRootFolder)
        self.btnSetRootFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnSetRootFolder.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btnSetRootFolder.setObjectName("btnSetRootFolder")
        self.layoutRootFolderSettings.addWidget(self.btnSetRootFolder)
        self.btnOpenRootFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenRootFolder.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btnOpenRootFolder.setObjectName("btnOpenRootFolder")
        self.layoutRootFolderSettings.addWidget(self.btnOpenRootFolder)
        self.verticalLayout.addLayout(self.layoutRootFolderSettings)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.layoutUpdateTaskIndicator = QtWidgets.QHBoxLayout()
        self.layoutUpdateTaskIndicator.setObjectName("layoutUpdateTaskIndicator")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 22))
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.layoutUpdateTaskIndicator.addWidget(self.progressBar)
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btnUpdate.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/download.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnUpdate.setIcon(icon1)
        self.btnUpdate.setObjectName("btnUpdate")
        self.layoutUpdateTaskIndicator.addWidget(self.btnUpdate)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.btnCancel.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/cancel.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnCancel.setIcon(icon2)
        self.btnCancel.setObjectName("btnCancel")
        self.layoutUpdateTaskIndicator.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.layoutUpdateTaskIndicator)
        self.layoutListVersions = QtWidgets.QVBoxLayout()
        self.layoutListVersions.setObjectName("layoutListVersions")
        self.verticalLayout.addLayout(self.layoutListVersions)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClearTempFolder = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/clear.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionClearTempFolder.setIcon(icon3)
        self.actionClearTempFolder.setObjectName("actionClearTempFolder")
        self.actionMinimizeToTray = QtWidgets.QAction(MainWindow)
        self.actionMinimizeToTray.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/tray.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMinimizeToTray.setIcon(icon4)
        self.actionMinimizeToTray.setObjectName("actionMinimizeToTray")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/quit.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionQuit.setIcon(icon5)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionClearTempFolder)
        self.menuFile.addAction(self.actionMinimizeToTray)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blender Version Manager"))
        self.labelRootFolder.setText(_translate("MainWindow", "No Root Folder Specified!"))
        self.btnSetRootFolder.setText(_translate("MainWindow", "Change"))
        self.btnOpenRootFolder.setText(_translate("MainWindow", "Open"))
        self.progressBar.setFormat(_translate("MainWindow", "No Tasks"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionClearTempFolder.setText(_translate("MainWindow", "Clear Temp Folder"))
        self.actionMinimizeToTray.setText(_translate("MainWindow", "Toggle Minimize to Tray"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

import resources_rc
