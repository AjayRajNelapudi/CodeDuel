import sys
import socket
from ftplib import FTP
import os

if os.name == 'nt':
    separator = '//'
else:
    separator = '/'

class File_Transfer:
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
        self.ftp.cwd('documents/codeduelcursors2019/spec')
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

    def __del__(self):
        self.ftp.quit()

def push_file(c_id, program_file):
    server = socket.socket()
    hostname, port = 'localhost', 32757
    server.connect((hostname, port))

    push_file = File_Transfer(c_id)
    push_file.upload_file(program_file)

    message = str(c_id) + ',' + program_file
    server.send(message.encode())

    test_run_status = server.recv(1024)
    print(test_run_status.decode())

    server.close()

def accept_challenge(p_title):
    pull_file = File_Transfer(-1)
    pull_file.download_file(p_title)

if len(sys.argv) == 2:
    accept_challenge(sys.argv[1])
elif len(sys.argv) == 3:
    push_file(int(sys.argv[1]), sys.argv[2])
else:
    print('Incorrect No of args')