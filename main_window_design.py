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
        MainWindow.resize(440, 240)
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
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow\n"
"{\n"
"    background-color: rgb(30, 30, 30);\n"
"}")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutTitleBar = QtWidgets.QHBoxLayout()
        self.layoutTitleBar.setContentsMargins(0, 0, -1, -1)
        self.layoutTitleBar.setSpacing(0)
        self.layoutTitleBar.setObjectName("layoutTitleBar")
        self.btnFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnFile.setSizeIncrement(QtCore.QSize(0, 0))
        self.btnFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnFile.setToolTip("File Menu")
        self.btnFile.setStatusTip("")
        self.btnFile.setAutoFillBackground(False)
        self.btnFile.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(60, 60, 60);\n"
"    border-style: solid;\n"
"    border-width: 6px 0px 6px 0px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"}\n"
"\n"
"QPushButton::menu-indicator \n"
"{\n"
"    image: none;\n"
"}")
        self.btnFile.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/app.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnFile.setIcon(icon1)
        self.btnFile.setIconSize(QtCore.QSize(20, 20))
        self.btnFile.setObjectName("btnFile")
        self.layoutTitleBar.addWidget(self.btnFile)
        self.title = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setAutoFillBackground(False)
        self.title.setStyleSheet("background-color: rgb(60, 60, 60);\n"
"color: rgb(204, 204, 204);\n"
"padding: 0px 0px 0px 20px;")
        self.title.setText("Blender Version Manager 1.2")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.title.setObjectName("title")
        self.layoutTitleBar.addWidget(self.title)
        self.btnMinimize = QtWidgets.QPushButton(self.centralwidget)
        self.btnMinimize.setSizeIncrement(QtCore.QSize(0, 0))
        self.btnMinimize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnMinimize.setToolTip("")
        self.btnMinimize.setStatusTip("")
        self.btnMinimize.setAutoFillBackground(False)
        self.btnMinimize.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(60, 60, 60);\n"
"    border-style: solid;\n"
"    border-width: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"}")
        self.btnMinimize.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMinimize.setIcon(icon2)
        self.btnMinimize.setIconSize(QtCore.QSize(20, 20))
        self.btnMinimize.setObjectName("btnMinimize")
        self.layoutTitleBar.addWidget(self.btnMinimize)
        self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        self.btnClose.setSizeIncrement(QtCore.QSize(0, 0))
        self.btnClose.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnClose.setToolTip("")
        self.btnClose.setStatusTip("")
        self.btnClose.setAutoFillBackground(False)
        self.btnClose.setStyleSheet("QPushButton\n"
"{\n"
"    background-color: rgb(60, 60, 60);\n"
"    border-style: solid;\n"
"    border-width: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(232, 17, 35);\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(232, 17, 35);\n"
"}")
        self.btnClose.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnClose.setIcon(icon3)
        self.btnClose.setIconSize(QtCore.QSize(20, 20))
        self.btnClose.setObjectName("btnClose")
        self.layoutTitleBar.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.layoutTitleBar)
        self.layoutRootFolderSettings = QtWidgets.QHBoxLayout()
        self.layoutRootFolderSettings.setContentsMargins(6, -1, 6, -1)
        self.layoutRootFolderSettings.setSpacing(0)
        self.layoutRootFolderSettings.setObjectName("layoutRootFolderSettings")
        self.labelRootFolder = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelRootFolder.sizePolicy().hasHeightForWidth())
        self.labelRootFolder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.labelRootFolder.setFont(font)
        self.labelRootFolder.setToolTip("Root Folder Path")
        self.labelRootFolder.setStatusTip("")
        self.labelRootFolder.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelRootFolder.setText("C:/Blender/2.8")
        self.labelRootFolder.setTextFormat(QtCore.Qt.PlainText)
        self.labelRootFolder.setScaledContents(False)
        self.labelRootFolder.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.labelRootFolder.setObjectName("labelRootFolder")
        self.layoutRootFolderSettings.addWidget(self.labelRootFolder)
        self.btnSetRootFolder = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetRootFolder.sizePolicy().hasHeightForWidth())
        self.btnSetRootFolder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnSetRootFolder.setFont(font)
        self.btnSetRootFolder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnSetRootFolder.setToolTip("Change Root Folder")
        self.btnSetRootFolder.setStatusTip("")
        self.btnSetRootFolder.setAutoFillBackground(False)
        self.btnSetRootFolder.setStyleSheet("QPushButton\n"
"{\n"
"    border-style: solid;\n"
"    border-width: 4px;\n"
"}\n"
"                 \n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}\n"
"                 \n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}")
        self.btnSetRootFolder.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/folder_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnSetRootFolder.setIcon(icon4)
        self.btnSetRootFolder.setIconSize(QtCore.QSize(20, 20))
        self.btnSetRootFolder.setFlat(True)
        self.btnSetRootFolder.setObjectName("btnSetRootFolder")
        self.layoutRootFolderSettings.addWidget(self.btnSetRootFolder)
        self.btnOpenRootFolder = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOpenRootFolder.sizePolicy().hasHeightForWidth())
        self.btnOpenRootFolder.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnOpenRootFolder.setFont(font)
        self.btnOpenRootFolder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnOpenRootFolder.setToolTip("Open Root Folder")
        self.btnOpenRootFolder.setStatusTip("")
        self.btnOpenRootFolder.setStyleSheet("QPushButton\n"
"{\n"
"    border-style: solid;\n"
"    border-width: 4px;\n"
"}\n"
"                 \n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}\n"
"                 \n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}")
        self.btnOpenRootFolder.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnOpenRootFolder.setIcon(icon5)
        self.btnOpenRootFolder.setIconSize(QtCore.QSize(20, 20))
        self.btnOpenRootFolder.setDefault(False)
        self.btnOpenRootFolder.setFlat(True)
        self.btnOpenRootFolder.setObjectName("btnOpenRootFolder")
        self.layoutRootFolderSettings.addWidget(self.btnOpenRootFolder)
        self.verticalLayout.addLayout(self.layoutRootFolderSettings)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setStyleSheet("margin: 0px 6px 0px 6px;\n"
"color:  rgb(97, 97, 98);")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.layoutUpdateTaskIndicator = QtWidgets.QHBoxLayout()
        self.layoutUpdateTaskIndicator.setContentsMargins(6, -1, 6, -1)
        self.layoutUpdateTaskIndicator.setSpacing(0)
        self.layoutUpdateTaskIndicator.setObjectName("layoutUpdateTaskIndicator")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.progressBar.setFont(font)
        self.progressBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.progressBar.setToolTip("")
        self.progressBar.setStatusTip("")
        self.progressBar.setStyleSheet("QProgressBar\n"
"{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(51, 51, 51);\n"
"    border-style: solid;\n"
"    border-color: rgb(51, 51, 51);\n"
"    border-width: 3px;\n"
"}\n"
"\n"
"QProgressBar::chunk \n"
"{\n"
"    background: rgb(49, 117, 52);\n"
"}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setFormat("No Tasks")
        self.progressBar.setObjectName("progressBar")
        self.layoutUpdateTaskIndicator.addWidget(self.progressBar)
        self.btnUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.btnUpdate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnUpdate.setToolTip("Start Downloading")
        self.btnUpdate.setStatusTip("")
        self.btnUpdate.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(51, 51, 51);\n"
"    border-style: solid;\n"
"    border-color: rgb(51, 51, 51);\n"
"    border-width: 4px;\n"
"}\n"
"                 \n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}\n"
"                 \n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}")
        self.btnUpdate.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnUpdate.setIcon(icon6)
        self.btnUpdate.setIconSize(QtCore.QSize(20, 20))
        self.btnUpdate.setFlat(True)
        self.btnUpdate.setObjectName("btnUpdate")
        self.layoutUpdateTaskIndicator.addWidget(self.btnUpdate)
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCancel.setToolTip("Cancel Downloading")
        self.btnCancel.setStatusTip("")
        self.btnCancel.setStyleSheet("QPushButton\n"
"{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(51, 51, 51);\n"
"    border-style: solid;\n"
"    border-color: rgb(51, 51, 51);\n"
"    border-width: 4px;\n"
"}\n"
"                 \n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}\n"
"                 \n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(80, 80, 80);\n"
"    border-color: rgb(80, 80, 80);\n"
"}")
        self.btnCancel.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btnCancel.setIcon(icon7)
        self.btnCancel.setIconSize(QtCore.QSize(20, 20))
        self.btnCancel.setFlat(True)
        self.btnCancel.setObjectName("btnCancel")
        self.layoutUpdateTaskIndicator.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.layoutUpdateTaskIndicator)
        self.layoutListVersions = QtWidgets.QVBoxLayout()
        self.layoutListVersions.setObjectName("layoutListVersions")
        self.verticalLayout.addLayout(self.layoutListVersions)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 440, 21))
        self.menubar.setStyleSheet("")
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menuFile.setStyleSheet("QMenu\n"
"{\n"
"    background-color: rgb(37, 37, 38);\n"
"    color: rgb(255, 255, 255);\n"
"    padding: 4px 1px 4px 1px;\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    background-color: rgb(97, 97, 98);\n"
"    height: 1px;\n"
"    margin: 4px 8px 4px 32px;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 4px 12px 4px 32px;\n"
"}\n"
"\n"
"QMenu::item::selected\n"
"{\n"
"    background-color: rgb(9, 71, 113);\n"
"}\n"
"\n"
"QMenu::icon \n"
"{\n"
"    margin: 6px;\n"
"}\n"
"\n"
"QMenu::icon:checked \n"
"{\n"
"    image: url(:/icons/tick.png);\n"
"}")
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStatusTip("")
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionClearTempFolder = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionClearTempFolder.setIcon(icon8)
        self.actionClearTempFolder.setText("Clear Temp Folder")
        self.actionClearTempFolder.setIconText("Clear Temp Folder")
        self.actionClearTempFolder.setToolTip("Clear Temp Folder")
        self.actionClearTempFolder.setStatusTip("")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionClearTempFolder.setFont(font)
        self.actionClearTempFolder.setObjectName("actionClearTempFolder")
        self.actionMinimizeToTray = QtWidgets.QAction(MainWindow)
        self.actionMinimizeToTray.setCheckable(True)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/fake.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionMinimizeToTray.setIcon(icon9)
        self.actionMinimizeToTray.setText("Toggle Minimize to Tray")
        self.actionMinimizeToTray.setToolTip("Minimize to Tray")
        self.actionMinimizeToTray.setStatusTip("")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionMinimizeToTray.setFont(font)
        self.actionMinimizeToTray.setObjectName("actionMinimizeToTray")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionQuit.setIcon(icon10)
        self.actionQuit.setText("Quit                        Ctrl+Q")
        self.actionQuit.setToolTip("Quit")
        self.actionQuit.setStatusTip("")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionQuit.setFont(font)
        self.actionQuit.setObjectName("actionQuit")
        self.actionRunOnStartup = QtWidgets.QAction(MainWindow)
        self.actionRunOnStartup.setCheckable(True)
        self.actionRunOnStartup.setIcon(icon9)
        self.actionRunOnStartup.setToolTip("Run on Startup")
        self.actionRunOnStartup.setStatusTip("")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.actionRunOnStartup.setFont(font)
        self.actionRunOnStartup.setObjectName("actionRunOnStartup")
        self.menuFile.addAction(self.actionClearTempFolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionMinimizeToTray)
        self.menuFile.addAction(self.actionRunOnStartup)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Blender Version Manager 1.2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionRunOnStartup.setText(_translate("MainWindow", "Toggle Run on Startup"))

import resources_rc
