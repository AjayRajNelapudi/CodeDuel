from ftplib import FTP
import os

if os.name == 'nt':
    separator = '//'
else:
    separator = '/'

class FileUpload:
    def __init__(self, c_id):
        self.c_id = c_id

        self.ftp = FTP('')
        self.ftp.connect('', 1026)
        self.ftp.login()
        #self.ftp.retrlines('LIST')

    def upload_file(self, filename):
        self.ftp.cwd('documents/codeduelcursors2019/src' + separator + str(self.c_id) + separator + filename.split('.')[0])
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

    def download_file(self, filename):
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

    def __del__(self):
        self.ftp.quit()