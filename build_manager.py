import os
import re
import zipfile
from urllib.request import urlopen
from PyQt5.QtCore import QCoreApplication

from bs4 import BeautifulSoup

b3d_storage_path = 'D:/Blender Storage'
b3d_storage_temp_path = b3d_storage_path + '/temp'

# Get download URL from builder page
def get_url():
    builder_url = 'https://builder.blender.org'
    builder_content = urlopen(builder_url + '/download').read()
    builder_soup = BeautifulSoup(builder_content, 'html.parser')
    version_url = builder_soup.find(href=re.compile('blender-2.80'))['href']
    download_url = builder_url + version_url
    return download_url

# Load zip file to local disk
def load_zip(progress_bar, root_path):
    download_url = get_url()
    blender_zip = urlopen(download_url)
    size = blender_zip.info()['Content-Length']
    CHUNK = 16 * 1024
    download_path = root_path + '/' + download_url.split('/', -1)[-1]
    progress_bar.text = "Downloading"
    with open(download_path, 'wb') as f:
        while True:
            chunk = blender_zip.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
            loaded = os.stat(download_path).st_size / int(size)
            print('Downloading: ' + str(loaded * 100))
            progress_bar.setValue(loaded * 100)
            QCoreApplication.processEvents()

    # Extract zip file
    zf = zipfile.ZipFile(download_path)
    uncompress_size = sum((file.file_size for file in zf.infolist()))
    extracted_size = 0

    for file in zf.infolist():
        extracted_size += file.file_size
        percentage = extracted_size * 100 / uncompress_size
        print('Extracting: ' + str(percentage))
        zf.extract(file, b3d_storage_path)
        QCoreApplication.processEvents()
