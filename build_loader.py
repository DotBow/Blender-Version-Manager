import os
import re
import shutil
import subprocess
import time
import zipfile
from pathlib import Path
from subprocess import CREATE_NO_WINDOW, DEVNULL, PIPE, STDOUT
from urllib.request import urlopen

from PyQt5.QtCore import QThread, pyqtSignal


class BuildLoader(QThread):
    finished = pyqtSignal('PyQt_PyObject')
    block_abortion = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, parent, url):
        QThread.__init__(self)
        self.url = url
        self.parent = parent
        self.root_folder = self.parent.settings.value('root_folder')
        self.is_running = False

    def run(self):
        self.is_running = True
        blender_zip = urlopen(self.url)
        size = blender_zip.info()['Content-Length']
        temp_path = os.path.join(self.root_folder, "temp")
        path = os.path.join(temp_path, self.url.split('/', -1)[-1])

        # Create temp directory
        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

        # Download
        with open(path, 'wb') as file:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                file.write(chunk)
                self.progress_changed.emit(
                    os.stat(path).st_size / int(size), "Downloading: %p%")

                if not self.is_running:
                    file.close()
                    if os.path.isdir(temp_path):
                        shutil.rmtree(temp_path)
                    self.finished.emit(None)
                    return

        # Extract
        zf = zipfile.ZipFile(path)
        version = zf.infolist()[0].filename.split('/')[0]
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            zf.extract(file, self.root_folder)
            extracted_size += file.file_size
            self.progress_changed.emit(
                extracted_size / uncompress_size, "Extracting: %p%")

            if not self.is_running:
                shutil.rmtree(os.path.join(self.root_folder, version))
                zf.close()
                if os.path.isdir(temp_path):
                    shutil.rmtree(temp_path)
                self.finished.emit(None)
                return

        zf.close()
        self.block_abortion.emit()
        self.progress_changed.emit(0, "Finishing...")

        # Delete temp folder
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)

        # Get blender version info
        b3d_exe = os.path.join(self.root_folder, version, "blender.exe")

        info = subprocess.check_output(
            [b3d_exe, "-v"], creationflags=CREATE_NO_WINDOW, shell=True,
            stderr=DEVNULL, stdin=DEVNULL).decode('UTF-8')

        ctime = re.search("build commit time: " + "(.*)", info)[1].rstrip()
        cdate = re.search("build commit date: " + "(.*)", info)[1].rstrip()
        strptime = time.strptime(cdate + ' ' + ctime, "%Y-%m-%d %H:%M")

        # Make nice name for dir
        git = re.search("build hash: " + "(.*)", info)[1].rstrip()
        nice_name = "Git-%s-%s" % (git, time.strftime("%d-%b-%H-%M", strptime))

        p = Path(os.path.join(self.root_folder, version))
        t = Path(os.path.join(self.root_folder, nice_name))
        p.rename(t)

        # Register .blend extension
        test = t / "blender.exe"

        if self.parent.settings.value('is_register_blend', type=bool):
            subprocess.call([str(test), "-r"], creationflags=CREATE_NO_WINDOW,
                            shell=True, stdout=PIPE, stderr=STDOUT, stdin=DEVNULL)

        self.finished.emit(nice_name)

    def stop(self):
        self.is_running = False
