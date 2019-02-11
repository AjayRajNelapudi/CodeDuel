import socket
from contextlib import suppress
with suppress(Exception):
    from Server import runtime
    from Server import database

with suppress(Exception):
    import runtime
    import database

import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class Server:
    def __init__(self, database, client_conn, c_id, specs):
        self.c_id = c_id
        self.database = database
        self.client_conn = client_conn
        self.specs = specs

    def ftp_service(self):
        username = 'ajay'
        port = 12345
        authorizer = DummyAuthorizer()
        authorizer.add_user(username, port, "/users/ajayraj", perm="elradfmw")
        authorizer.add_anonymous("/users/ajayraj/", perm="elradfmw")

        handler = FTPHandler
        handler.authorizer = authorizer

        ftp_server = FTPServer(("", 1026), handler)
        ftp_server.serve_forever()

    def client_service(self):
        print('test')
        try:
            program_file = self.specs
            src_path = self.database.get_directory_path('src')
            test_path = self.database.get_directory_path('test')
            filename, extension = program_file.split('.')
            p_id = self.database.get_pid(filename)
            test_file_names = self.database.get_test_filenames(p_id)

            run = runtime.Run_Tests(self.c_id, program_file, src_path, test_path, test_file_names)
            test_run_status = run.run_tests()
            test_run_status = ' '.join(test_run_status)
            self.client_conn.send(test_run_status.encode())

            duel_id = self.database.get_duel_id(self.c_id)
            print('\n\n\n')
            print('Duel ID:', duel_id)
            print('Contestant ID:', self.c_id)
            print('Test Run:', test_run_status)
            print('\n\n\n')
        except:
            print('Testrun failed. Contact admin', self.c_id)

    def duel_scores(self):
        print('score')
        try:
            opponent_id = self.database.get_opponent_id(self.c_id)

            contestant_name = self.database.get_contestant_name(self.c_id)
            opponent_name = self.database.get_contestant_name(opponent_id)

            contestant_score = 0 if self.database.get_score(self.c_id) is None else self.database.get_score(self.c_id)
            opponent_score = 0 if self.database.get_score(opponent_id) is None else self.database.get_score(opponent_id)

            message = contestant_name + ' -> ' + str(contestant_score) + '\n' + opponent_name + ' -> ' + str(opponent_score)
            '''leaderboard = self.database.make_duel_leaderboard()
            message = ''
            for contestant in leaderboard:
                for attribute in contestant:
                    message += str(attribute) + '\t'
                message += '\n'
            '''
            self.client_conn.send(message.encode())
        except Exception as e:
            print('Error in retrieveing scores. Contact admin', self.c_id, e)

    def validate_login(self):
        print('login')
        try:
            if self.database.validate_login(self.c_id, specs):
                message = 'success'
            else:
                message = 'fail'

            self.client_conn.send(message.encode())
        except:
            print('Login Credentials Incorrect', self.c_id)

    def __del__(self):
        with suppress(Exception):
            self.client_conn.close()

hostname, port = '', 32757
server = socket.socket()
server.bind((hostname, port))
server.listen(10)

ftp_server = Server(None, None, None, None)
ftp_service_thread = threading.Thread(target=ftp_server.ftp_service)
ftp_service_thread.start()

while True:
    conn, addr = server.accept()
    print('\n', conn, addr, '\n')
    received_message = conn.recv(port).decode()

    try:
        action, c_id, specs = received_message.split(',')

        codeduel_db = database.CodeDuel_Database()
        server_interface = Server(codeduel_db, conn, c_id, specs)

        if action == 'score':
            duel_scores_thread = threading.Thread(target=server_interface.duel_scores)
            duel_scores_thread.start()
        elif action == 'test':
            client_service_thread = threading.Thread(target=server_interface.client_service)
            client_service_thread.start()
        elif action == 'validate':
            validate_thread = threading.Thread(target=server_interface.validate_login)
            validate_thread.start()
    except:
        conn.close()
