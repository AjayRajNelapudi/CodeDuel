import sys
import socket
from ftplib import FTP
import os
import json

if os.name == 'nt':
    separator = '\\'
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
        file, dir = filename.split('.')
        self.ftp.cwd('documents/codeduelcursors2019/src' + separator + str(self.c_id) + separator + file)
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

    def download_file(self, filename):
        file, extension = filename.split('.')
        self.ftp.cwd('documents/codeduelcursors2019/spec' + separator + file)
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

    def __del__(self):
        self.ftp.quit()

def validate_login(c_id, password):
    server = socket.socket()
    hostname, port = 'localhost', 32757
    server.connect((hostname, port))

    message = 'validate,' + str(c_id) + ',' + password
    server.send(message.encode())

    response = server.recv(1024)
    server.close()
    if response.decode() == 'success':
        return True
    return False

def push_file(c_id, program_file):
    server = socket.socket()
    hostname, port = 'localhost', 32757
    server.connect((hostname, port))

    push_file = File_Transfer(c_id)
    push_file.upload_file(program_file)

    message = 'client,' + str(c_id) + ',' + program_file
    server.send(message.encode())

    test_run_status = server.recv(1024)
    server.close()
    return 'Test Run: ' + test_run_status.decode()

def accept_challenge(p_title):
    pull_file = File_Transfer(-1)
    pull_file.download_file(p_title)

def get_duel_scores(c_id):
    server = socket.socket()
    hostname, port = 'localhost', 32757
    server.connect((hostname, port))

    message = 'client,' + str(c_id) + ',' + 'SCORE'
    server.send(message.encode())
    scores = server.recv(1024).decode()
    server.close()
    return scores

def get_cid():
    pass

def print_help():
    help = '''
To accept a challenge:
python3 client.py pull <TitleOfTheProblem.txt>

To push a script and get results:
python3 client.py push <filename with extension>

To view yours and your opponent's points:
python3 client.py points
            '''
    print(help)

def configure(c_id):
    metadata = dict()
    metadata['c_id'] = c_id
    with open('metadata.json', 'w') as metadata_file:
        json.dump(metadata, metadata_file)

def read_c_id(metadata_filename):
    try:
        with open(metadata_filename) as metadata_file:
            metadata = json.load(metadata_file)
            c_id = metadata['c_id']
        return c_id
    except:
        print('config before first use')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Wrong usage")
        sys.exit(0)

    argc = len(sys.argv)
    if sys.argv[1] == 'push' and argc > 2:
        c_id = read_c_id('metadata.json')
        for i in range(2, argc):
            test_run_status = push_file(c_id, sys.argv[i])
            print(test_run_status)
    elif sys.argv[1] == 'pull' and argc == 3:
        c_id = read_c_id('metadata.json')
        accept_challenge(sys.argv[2])
    elif sys.argv[1] == 'points' and argc == 2:
        c_id = read_c_id('metadata.json')
        points = get_duel_scores(c_id)
        print(points)
    elif sys.argv[1] == 'config' and argc == 3:
        configure(int(sys.argv[2]))
    else:
        print('Incorrect args usage')
        print_help()


