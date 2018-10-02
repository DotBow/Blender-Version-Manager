import os
import shutil
import zipfile
from urllib.request import urlopen

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication


class BuildLoader(QObject):
    finished = pyqtSignal('PyQt_PyObject')
    progress_changed = pyqtSignal('PyQt_PyObject', 'PyQt_PyObject')

    def __init__(self, root_folder, download_url):
        QObject.__init__(self)
        self.download_url = download_url
        self.root_folder = root_folder
        self.is_running = False

    def run(self):
        self.is_running = True
        blender_zip = urlopen(self.download_url)
        size = blender_zip.info()['Content-Length']
        temp_path = os.path.join(self.root_folder, "temp")

        if not os.path.isdir(temp_path):
            os.makedirs(temp_path)

        download_path = os.path.join(
            temp_path, self.download_url.split('/', -1)[-1])

        with open(download_path, 'wb') as self.f:
            while True:
                QApplication.processEvents()
                chunk = blender_zip.read(16 * 1024)

                if not chunk:
                    break

                self.f.write(chunk)
                self.progress_changed.emit(
                    os.stat(download_path).st_size / int(size), "Downloading")

                if not self.is_running:
                    self.f.close()
                    os.remove(download_path)
                    self.finished.emit(False)
                    return

        zf = zipfile.ZipFile(download_path)
        uncompress_size = sum((file.file_size for file in zf.infolist()))
        extracted_size = 0

        for file in zf.infolist():
            QApplication.processEvents()
            zf.extract(file, self.root_folder)
            extracted_size += file.file_size
            self.progress_changed.emit(
                extracted_size / uncompress_size, "Extracting")

            if not self.is_running:
                shutil.rmtree(os.path.join(self.root_folder,
                                           zf.infolist()[0].filename.split('/')[0]))
                zf.close()
                os.remove(download_path)
                self.finished.emit(False)
                return

        self.finished.emit(True)

    def stop(self):
        self.is_running = False
