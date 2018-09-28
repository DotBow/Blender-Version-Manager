import os
import zipfile
from urllib.request import urlopen

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal


class BuildLoader(QThread):
    finished = pyqtSignal()
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, root_folder, download_url):
        QThread.__init__(self)
        self.download_url = download_url
        self.root_folder = root_folder

    def run(self):
        blender_zip = urlopen(self.download_url)
        size = blender_zip.info()['Content-Length']
        temp_path = os.path.join(self.root_folder, "temp")

        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

        download_path = os.path.join(
            temp_path, self.download_url.split('/', -1)[-1])

        with open(download_path, 'wb') as f:
            while True:
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                f.write(chunk)
                self.progress_changed.emit(
                    os.stat(download_path).st_size / int(size), "Downloading")

        zf = zipfile.ZipFile(download_path)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            zf.extract(file, self.root_folder)
            extracted_size += file.file_size
            self.progress_changed.emit(
                extracted_size / uncompress_size, "Extracting")

        self.finished.emit()

    def stop(self):
        self.terminate()
        self.finished.emit()
