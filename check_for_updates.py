import re
import time
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal

from _platform import get_platform


class CheckForUpdates(QThread):
    new_version_obtained = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.is_running = True
        self.download_url = None

    def run(self):
        while self.is_running:
            try:
                self.download_url = self.get_download_url()
                commit = self.download_url.split('-',)[2]
                new_version = True

                if self.parent.layouts:
                    if (commit in self.parent.layouts[0].git or commit in self.parent.progressBar.text()):
                        new_version = False

                if new_version:
                    datetime = self.get_commit_datetime(commit)
                    self.strptime = time.strptime(
                        datetime, '%a, %d %b %Y %H:%M:%S %z')
                    strftime = time.strftime("%d-%b-%H:%M", self.strptime)
                    info = urlopen(self.download_url).info()
                    size = str(int(info['content-length']) // 1048576) + " MB"
                    display_name = "Git-" + commit + " | " + strftime + " | " + size
                    self.new_version_obtained.emit(display_name)
            except urllib.error.URLError as e:
                print(e)

            QThread.sleep(600)

        return

    def get_download_url(self):
        builder_url = "https://builder.blender.org"
        content = urlopen(builder_url + "/download").read()
        soup = BeautifulSoup(content, 'html.parser')
        platform = get_platform()

        if platform == 'Windows':
            build_url = soup.find(href=re.compile(
                r'blender-.+win64'))['href']
        elif platform == 'Linux':
            build_url = soup.find(href=re.compile(
                r'blender-.+linux.+64'))['href']

        return builder_url + build_url

    def get_commit_datetime(self, commit):
        commit_url = "https://git.blender.org/gitweb/gitweb.cgi/blender.git/commit/"
        content = urlopen(commit_url + commit).read()
        soup = BeautifulSoup(content, 'html.parser')
        datetime = soup.find_all("span", {"class": "datetime"})[1].text
        return datetime
