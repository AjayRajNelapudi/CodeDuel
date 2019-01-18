import socket
try:
    from Server import runtime
    from Server import database
except:
    pass

try:
    import runtime
    import database
except:
    pass

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

    ftp_server = FTPServer(("127.0.0.1", 1026), handler)
    ftp_server.serve_forever()

ftp_service_thread = threading.Thread(target=ftp_service)
ftp_service_thread.start()

hostname, port = 'localhost', 32757
server = socket.socket()
server.bind((hostname, port))
server.listen(10)

while True:
    def client_service(conn, program_file):
        src_path = database.get_directory_path('src')
        test_path = database.get_directory_path('test')
        p_id = database.get_pid(program_file.split('.')[0])
        test_file_names = database.get_test_filenames(p_id)

        run = runtime.Run_Tests(c_id, program_file, src_path, test_path, test_file_names)
        test_run_status = run.run_tests()
        test_run_status = ' '.join(test_run_status)

        conn.send(test_run_status.encode())
        conn.close()


    conn, addr = server.accept()
    received_message = conn.recv(port).decode()
    user_type, c_id, request = received_message.split(',')

    if user_type == 'client':
        client_service_thread = threading.Thread(target=client_service, args=(conn, request))
        client_service_thread.start()