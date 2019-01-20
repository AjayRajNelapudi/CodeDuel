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

def ftp_service():
    username = 'ajay'
    port = 12345
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, port, "/users/ajayraj", perm="elradfmw")
    authorizer.add_anonymous("/users/ajayraj/", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    ftp_server = FTPServer(("", 1026), handler)
    ftp_server.serve_forever()

ftp_service_thread = threading.Thread(target=ftp_service)
ftp_service_thread.start()

hostname, port = '', 32757
server = socket.socket()
server.bind((hostname, port))
server.listen(10)

while True:
    def client_service(conn, c_id, program_file):
        src_path = database.get_directory_path('src')
        test_path = database.get_directory_path('test')
        p_id = database.get_pid(program_file.split('.')[0])
        test_file_names = database.get_test_filenames(p_id)

        run = runtime.Run_Tests(c_id, program_file, src_path, test_path, test_file_names)
        test_run_status = run.run_tests()
        test_run_status = ' '.join(test_run_status)

        conn.send(test_run_status.encode())
        conn.close()

        duel_id = database.get_duel_id(c_id)
        print('\n\n\n')
        print('Duel ID:', duel_id)
        print('Contestant ID:', c_id)
        print('Test Run:', test_run_status)
        print('\n\n\n')

    def duel_scores(conn, c_id):
        opponent_id = database.get_opponent_id(c_id)

        contestant_name = database.get_contestant_name(c_id)
        opponent_name = database.get_contestant_name(opponent_id)

        contestant_score = 0 if database.get_score(c_id) is None else database.get_score(c_id)
        opponent_score = 0 if database.get_score(opponent_id) is None else database.get_score(opponent_id)

        message = contestant_name + ' -> ' + str(contestant_score) + '\n' + opponent_name + ' -> ' + str(opponent_score)
        conn.send(message.encode())

        conn.close()

    def validate_login(conn, c_id, password):
        if database.validate_login(c_id, password):
            message = 'success'
        else:
            message = 'fail'

        conn.send(message.encode())
        conn.close()


    conn, addr = server.accept()
    received_message = conn.recv(port).decode()
    try:
        user_type, c_id, file = received_message.split(',')

        if user_type == 'client':
            if file == 'SCORE':
                duel_scores_thread = threading.Thread(target=duel_scores, args=(conn, c_id))
                duel_scores_thread.start()
            else:
                client_service_thread = threading.Thread(target=client_service, args=(conn, c_id, file))
                client_service_thread.start()

        elif user_type == 'validate':
            validate_thread = threading.Thread(target=validate_login, args=(conn, c_id, file))
            validate_thread.start()
    except:
        conn.close()
