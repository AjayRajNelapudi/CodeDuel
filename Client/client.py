#!/Library/Frameworks/Python.framework/Versions/3.6/Python
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
        try:
            self.ftp.cwd('documents/codeduelcursors2019/src' + separator + str(self.c_id) + separator + file)
        except:
            self.ftp.cwd('documents/codeduelcursors2019/src' + separator + str(self.c_id))
        self.ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

    def download_file(self, filename):
        file, extension = filename.split('.')
        self.ftp.cwd('documents/codeduelcursors2019/spec' + separator + file)
        localfile = open(filename, 'wb')
        self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        localfile.close()

    def __del__(self):
        self.ftp.quit()

class Command:
    def __init__(self):
        self.server = socket.socket()
        hostname, port = 'localhost', 32757
        self.server.connect((hostname, port))

        try:
            self.read_c_id('metadata.json')
        except:
            pass

    def read_c_id(self, metadata_filename):
        with open(metadata_filename) as metadata_file:
            metadata = json.load(metadata_file)
            c_id = metadata['c_id']
        self.c_id = c_id

    def validate_login(self, c_id, password):
        message = 'validate,' + str(c_id) + ',' + password
        self.server.send(message.encode())

        response = self.server.recv(1024)

        if response.decode() == 'success':
            return True
        return False


    def configure(self, c_id, password):
        if not self.validate_login(c_id, password):
            print('Login Failed. Check Credentails')
            return

        self.c_id = c_id
        metadata = dict()
        metadata['c_id'] = c_id
        metadata['password'] = password
        with open('metadata.json', 'w') as metadata_file:
            json.dump(metadata, metadata_file)
        print('Login Successful')

    def push_file(self, program_file):
        try:
            self.read_c_id('metadata.json')
        except:
            print('Config before use')
            return

        try:
            push_file = File_Transfer(self.c_id)
            push_file.upload_file(program_file)

            message = 'test,' + str(self.c_id) + ',' + program_file
            self.server.send(message.encode())

            test_run_status = self.server.recv(1024)
            return 'Test Run: ' + test_run_status.decode()
        except:
            print('File Not Found')

    def accept_challenge(self, p_title):
        try:
            #self.read_c_id('metadata.json')
            pull_file = File_Transfer(-1)
            pull_file.download_file(p_title)
        except:
            print('Config before use')

    def get_duel_scores(self):
        try:
            self.read_c_id('metadata.json')
            message = 'score,' + str(self.c_id) + ','
            self.server.send(message.encode())
            scores = self.server.recv(1024).decode()

            return scores
        except:
            print('Config before use')

    def print_help(self):
        help = '''
Manually insert the data into database using MySQL statements.

Navigate to folder containting the source code:
To setup file-system:
python3 ServerAid/buildfiles.py

To run the server:
python3 Server/server.py

To confiure your id:
python3 client.py config <id> <password>

To accept a challenge:
python3 client.py pull <TitleOfTheProblem.txt>

To push a script and get results:
python3 client.py push <filename with extension>

To view yours and your opponent's points:
python3 client.py points
                '''
        print(help)

    def __del__(self):
        self.server.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Wrong usage")
        sys.exit(0)

    cmd = Command()
    argc = len(sys.argv)
    if sys.argv[1] == 'push' and argc > 2:
        for i in range(2, argc):
            test_run_status = cmd.push_file(sys.argv[i])
            if test_run_status is not None:
                print(test_run_status)
    elif sys.argv[1] == 'pull' and argc == 3:
        cmd.accept_challenge(sys.argv[2])
    elif sys.argv[1] == 'points' and argc == 2:
        points = cmd.get_duel_scores()
        print(points)
    elif sys.argv[1] == 'config' and argc == 4:
        cmd.configure(int(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == 'help' and argc == 2:
        cmd.print_help()
    else:
        print('Incorrect args usage')
        cmd.print_help()


