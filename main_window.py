import os
import re
import shutil
import subprocess
import sys
import webbrowser

from bs4 import BeautifulSoup
from PyQt5.QtCore import QEvent, QPoint, QSettings, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QMainWindow, QMenu, QMessageBox, QSizePolicy,
                             QSystemTrayIcon)

import main_window_design
from _platform import get_platform
from build_loader import BuildLoader
from check_for_updates import CheckForUpdates
from version_layout import B3dItemLayout

if get_platform() == 'Windows':
    import winreg
    from PyQt5.QtWinExtras import QWinTaskbarButton


class BVMQMainWindow(QMainWindow, main_window_design.Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)

        # Read icons
        self.icon_app = QIcon(":/icons/app.svg")
        self.icon_star = QIcon(":/icons/star.png")
        self.icon_trash = QIcon(":/icons/delete.png")
        self.icon_quit = QIcon(":/icons/quit.png")
        self.icon_fake = QIcon(":/icons/fake.svg")

        # Read settings
        self.settings = QSettings('b3d_version_manager', 'settings')

        is_register_blend = self.settings.value(
            'is_register_blend', type=bool)
        self.is_run_minimized = self.settings.value(
            'is_run_minimized', type=bool)
        is_run_on_startup = self.settings.value(
            'is_run_on_startup', type=bool)
        root_folder = self.settings.value('root_folder')
        if (not root_folder) or (not os.path.isdir(root_folder)):
            exe_path = os.path.dirname(sys.executable)
            self.settings.setValue('root_folder', exe_path)

        # Custom title bar
        self.btnWiki.clicked.connect(lambda: webbrowser.open(
            "https://github.com/DotBow/Blender-Version-Manager/wiki"))
        self.title.setText("%s %s" % (
            QApplication.applicationName(), QApplication.applicationVersion()))
        self.btnClose.clicked.connect(self.hide)
        self.btnMinimize.clicked.connect(self.showMinimized)

        # Custom menu bar
        self.actionToggleRegisterBlend.setChecked(is_register_blend)
        self.actionToggleRegisterBlend.triggered.connect(
            self.toggle_register_blend)

        self.actionToggleRunMinimized.setChecked(self.is_run_minimized)
        self.actionToggleRunMinimized.triggered.connect(
            self.toggle_run_minimized)

        self.actionToggleRunOnStartup.setChecked(is_run_on_startup)
        self.actionToggleRunOnStartup.triggered.connect(
            self.toggle_run_on_startup)

        self.menubar.hide()
        self.btnSettings.setMenu(self.menuFile)

        self.menuFile.installEventFilter(self)

        # Root folder layout
        self.labelRootFolder.setText(self.settings.value('root_folder'))
        self.btnSetRootFolder.clicked.connect(self.set_root_folder)
        self.btnOpenRootFolder.clicked.connect(self.open_root_folder)

        # Tray layout
        self.blender_action = QAction(self.icon_star, "Blender    ", self)
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        quit_action = QAction(self.icon_quit, "Quit", self)

        self.blender_action.triggered.connect(self.open_latest_b3d)
        show_action.triggered.connect(self.bring_to_front)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit)

        self.tray_menu = QMenu()
        self.tray_menu.setStyleSheet(self.menuFile.styleSheet())
        self.tray_menu.addAction(self.blender_action)
        self.tray_menu.addAction(show_action)
        self.tray_menu.addAction(hide_action)
        self.tray_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self.icon_app, self)
        self.tray_icon.setToolTip("Blender Version Manager")
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.messageClicked.connect(self.bring_to_front)
        self.tray_icon.activated.connect(self.onTrayIconActivated)
        self.tray_icon.show()

        # Version layout
        self.btnUpdate.clicked.connect(self.update)
        self.set_task_visible(False)
        self.zeroBuildsWarning.hide()
        self.layouts = []
        self.collect_versions()
        self.draw_list_versions()

        # Custom drag behaviour
        self.old_pos = self.pos()
        self.pressed = False

        # Update task
        self.is_update_running = False
        self.start_uptodate_thread()

        self.taskbar_progress = None

        self.left_click_timer = QTimer(self)
        self.left_click_timer.setSingleShot(True)
        self.left_click_timer.timeout.connect(self.bring_to_front)

    def start_uptodate_thread(self):
        self.uptodate_thread = CheckForUpdates(self)
        self.uptodate_thread.new_version_obtained.connect(
            self.show_new_version)
        self.uptodate_thread.start()

    def stop_uptodate_thread(self):
        self.uptodate_thread.is_running = False
        self.uptodate_thread.terminate()
        self.uptodate_thread.wait()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.left_click_timer.start(QApplication.doubleClickInterval())
        elif reason == QSystemTrayIcon.DoubleClick:
            self.left_click_timer.stop()
            self.open_latest_b3d()

    def showEvent(self, event):
        # Setup taskbar
        if not self.taskbar_progress:
            self.task_button = QWinTaskbarButton(self)
            self.task_button.setWindow(self.windowHandle())

            self.taskbar_progress = self.task_button.progress()
            self.taskbar_progress.setVisible(True)
            self.taskbar_progress.setValue(0)

    def open_latest_b3d(self):
        if self.layouts:
            self.layouts[0].open()

    def show_new_version(self, display_name):
        self.set_task_visible(True)
        self.set_progress_bar(0, 0, display_name)

        if self.isHidden():
            self.tray_icon.showMessage(
                "Blender Version Manager",
                "New version of Blender 2.8 is avaliable!",
                QSystemTrayIcon.Information, 4000)

    def set_task_visible(self, is_visible):
        if is_visible:
            self.progressBar.show()
            self.btnUpdate.show()
            self.btnCancel.hide()
        else:
            self.progressBar.hide()
            self.btnUpdate.hide()
            self.btnCancel.hide()

    def is_running_task(self):
        if self.is_update_running:
            QMessageBox.information(
                self, "Warning", "Update task in progress!", QMessageBox.Ok)
            return True
        else:
            return False

    def toggle_run_minimized(self, is_checked):
        self.settings.setValue('is_run_minimized', is_checked)

    def toggle_register_blend(self, is_checked):
        self.settings.setValue('is_register_blend', is_checked)

    def cleanup_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()
            else:
                self.cleanup_layout(item.layout())

    def collect_versions(self):
        self.layouts.clear()
        root_folder = self.settings.value('root_folder')
        dirs = next(os.walk(root_folder))[1]
        versions = []
        platform = get_platform()

        if platform == 'Windows':
            blender_exe = "blender.exe"
        elif platform == 'Linux':
            blender_exe = "blender"

        for dir in dirs:
            if os.path.isfile(os.path.join(root_folder, dir, blender_exe)):
                versions.append(dir)

        for ver in versions:
            b3d_item_layout = B3dItemLayout(
                root_folder, ver, False, self)
            self.layouts.append(b3d_item_layout)

    def draw_list_versions(self):
        if len(self.layouts) > 0:
            self.zeroBuildsWarning.hide()
            self.layouts.sort(key=lambda ver: ver.mtime, reverse=True)
            self.blender_action.setVisible(True)

            for b3d_item_layout in self.layouts:
                self.layoutListVersions.removeItem(b3d_item_layout)
                b3d_item_layout.set_is_latest(False)

            self.layouts[0].set_is_latest(True)

            for b3d_item_layout in self.layouts:
                self.layoutListVersions.addLayout(b3d_item_layout)
        else:
            self.zeroBuildsWarning.show()
            self.blender_action.setVisible(False)

    def set_root_folder(self):
        root_folder = self.settings.value('root_folder')
        dir = QFileDialog.getExistingDirectory(
            self, "Choose Root Folder", root_folder)

        if dir and (dir != root_folder):
            self.stop_uptodate_thread()
            self.zeroBuildsWarning.hide()
            self.set_task_visible(False)
            self.settings.setValue('root_folder', dir)
            self.labelRootFolder.setText(dir)
            self.cleanup_layout(self.layoutListVersions)
            self.collect_versions()
            self.draw_list_versions()
            self.start_uptodate_thread()

    def open_root_folder(self):
        platform = get_platform()
        root_folder = self.settings.value('root_folder')

        if platform == 'Windows':
            os.startfile(root_folder)
        elif platform == 'Linux':
            subprocess.call(["xdg-open", root_folder])

    def update(self):
        self.is_update_running = True
        self.stop_uptodate_thread()

        self.btnUpdate.hide()
        self.btnCancel.show()
        self.btnSetRootFolder.hide()
        self.set_progress_bar(0, 0, "Downloading: %p%")

        self.build_loader = BuildLoader(
            self, self.uptodate_thread.download_url, self.uptodate_thread.strptime)
        self.build_loader.finished.connect(self.finished)
        self.build_loader.progress_changed.connect(self.set_progress_bar)
        self.build_loader.block_abortion.connect(lambda: self.btnCancel.hide())
        self.btnCancel.clicked.connect(self.build_loader.stop)
        self.build_loader.start()

    def finished(self, version):
        self.build_loader.terminate()
        self.build_loader.wait()

        self.btnSetRootFolder.show()
        self.set_task_visible(False)
        self.is_update_running = False

        if version:
            root_folder = self.settings.value('root_folder')
            b3d_item_layout = B3dItemLayout(
                root_folder, version, True, self)
            self.layouts.append(b3d_item_layout)

            self.tray_icon.showMessage(
                "Blender Version Manager",
                "Update finished!",
                QSystemTrayIcon.Information, 4000)

        self.draw_list_versions()
        self.set_progress_bar(0, 0, "")
        self.start_uptodate_thread()

    def set_progress_bar(self, progress_bar_val, taskbar_val, format):
        self.progressBar.setFormat(format)
        self.progressBar.setValue(progress_bar_val * 100)

        if self.taskbar_progress:
            self.taskbar_progress.setValue(taskbar_val * 100)

    def quit(self):
        if not self.is_running_task():
            self.tray_icon.hide()
            self.app.quit()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def toggle_run_on_startup(self, is_checked):
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
                             0, winreg.KEY_SET_VALUE)

        if (is_checked):
            path = sys.executable
            winreg.SetValueEx(key, 'Blender Version Manager',
                              0, winreg.REG_SZ, path)
        else:
            try:
                winreg.DeleteValue(key, 'Blender Version Manager')
            except:
                pass

        key.Close()
        self.settings.setValue('is_run_on_startup', is_checked)

    def bring_to_front(self):
        self.setWindowState(self.windowState() & ~
                            Qt.WindowMinimized | Qt.WindowActive)
        self.show()
        self.activateWindow()

    # Prevent QMenu from closing
    def eventFilter(self, obj, event):
        if event.type() in [QEvent.MouseButtonRelease]:
            if isinstance(obj, QMenu):
                if obj.activeAction():
                    if not obj.activeAction().menu():
                        obj.activeAction().trigger()
                        return True

        return super(BVMQMainWindow, self).eventFilter(obj, event)
