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
        self.ftp.connect('localhost', 1026)
        self.ftp.login()
        self.ftp.cwd('/users/ajayraj/documents/codeduel/src/' + separator + str(self.c_id))
        self.ftp.retrlines('LIST')

    def uploadFile(self, filename):
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
        self.ftp.quit()

    def downloadFile(self, filename):
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        self.ftp.quit()
        localfile.close()
