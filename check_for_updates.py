import os
import re
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QSystemTrayIcon


class CheckForUpdates(QThread):
    new_version_obtained = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.is_running = False
        self.download_url = None
        self.test = True

    def run(self):
        while self.test:
            self.is_running = True

            try:
                self.download_url = self.get_download_url()
                version = self.download_url.split('-',)[-2]
                new_version = True

                if self.parent.latest_local:
                    if version in self.parent.latest_local:
                        new_version = False

                if new_version:
                    info = urlopen(self.download_url).info()
                    ctime = info['last-modified']
                    size = str(int(info['content-length']) // 1048576) + " MB"
                    display_name = "Git-" + version + " | " + ctime + " | " + size
                    self.new_version_obtained.emit(display_name)
            except urllib.error.URLError as e:
                print(e)

            print("Check For Updates")
            self.is_running = False
            QThread.sleep(5)

        self.terminate()

    def get_download_url(self):
        builder_url = "https://builder.blender.org"
        builder_content = urlopen(builder_url + "/download").read()
        builder_soup = BeautifulSoup(builder_content, 'html.parser')
        version_url = builder_soup.find(
            href=re.compile("blender-2.80"))['href']
        return builder_url + version_url

    def stop(self):
        self.test = False
