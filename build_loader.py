import os
import shutil
import subprocess
import time
import zipfile
from urllib.request import urlopen

from PyQt5.QtCore import QThread, pyqtSignal


class BuildLoader(QThread):
    finished = pyqtSignal('PyQt_PyObject')
    block_abortion = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, parent, download_url):
        QThread.__init__(self)
        self.download_url = download_url
        self.parent = parent
        self.root_folder = self.parent.settings.value('root_folder')
        self.is_running = False

    def run(self):
        self.is_running = True
        blender_zip = urlopen(self.download_url)
        size = blender_zip.info()['Content-Length']
        temp_path = os.path.join(self.root_folder, "temp")
        download_path = os.path.join(
            temp_path, self.download_url.split('/', -1)[-1])

        # Create temp directory
        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

        # Get time in seconds
        ctime = urlopen(self.download_url).info()['last-modified']
        strptime = time.strptime(ctime, '%a, %d %b %Y %H:%M:%S %Z')
        mod_time = time.mktime(strptime)

        # Download
        with open(download_path, 'wb') as self.f:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                self.f.write(chunk)
                self.progress_changed.emit(
                    os.stat(download_path).st_size / int(size), "Downloading: %p%")

                if not self.is_running:
                    self.f.close()
                    if os.path.isdir(temp_path):
                        shutil.rmtree(temp_path)
                    self.finished.emit(False)
                    return

        # Extract
        zf = zipfile.ZipFile(download_path)
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
                self.finished.emit(False)
                return

        zf.close()
        self.block_abortion.emit()

        # Delete temp folder
        self.progress_changed.emit(0, "Deleting temporary files...")
        if os.path.isdir(temp_path):
            shutil.rmtree(temp_path)

        # Make nice name for dir
        self.progress_changed.emit(0, "Making nice naming...")
        git = (version.split("git.", 2)[-1]).split('-',)[0]
        nice_name = "Git-" + git + "-" + time.strftime("%d-%b-%H-%M", strptime)
        os.rename(os.path.join(self.root_folder, version),
                  os.path.join(self.root_folder, nice_name))
        version = nice_name

        # Change time to match one from BuildBot
        self.progress_changed.emit(0, "Matching time with BuildBot...")
        os.utime(os.path.join(self.root_folder,
                              version, "blender.exe"), (mod_time, mod_time))

        # Register .blend extension
        if self.parent.settings.value('is_register_blend', type=bool):
            self.progress_changed.emit(0, "Registering .blend extension...")
            path = os.path.join(self.root_folder, version, "blender.exe")
            subprocess.call(
                [path, "-r"], creationflags=subprocess.CREATE_NO_WINDOW)

        self.progress_changed.emit(0, "Finishing...")
        self.finished.emit(True)

    def stop(self):
        self.is_running = False
