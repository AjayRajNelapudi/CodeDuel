import sys
import socket
from ftplib import FTP
import os

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
        self.ftp.cwd('documents/codeduelcursors2019/spec')
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

def print_help():
    help = '''
To accept a challenge:
python3 client.py <TitleOfTheProblem.txt>

To push a script and get results:
python3 client.py <id> <filename with extension>

To view yours and your opponent's points:
python3 client.py <your id> points
            '''
    print(help)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        if sys.argv[1] == 'help':
            print_help()
        else:
            accept_challenge(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[2] == 'points':
            scores = get_duel_scores(int(sys.argv[1]))
            print(scores)
        else:
            test_run_status = push_file(int(sys.argv[1]), sys.argv[2])
            print(test_run_status)
    else:
        print('Incorrect no of args')
