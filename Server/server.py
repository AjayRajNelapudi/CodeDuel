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
    def service(conn, addr, received_message):
        c_id, program_file = received_message.split(',')

        src_path = database.get_directory_path('src')
        tests_path = database.get_directory_path('test')
        p_id = database.get_pid(program_file.split('.')[0])
        test_file_names = database.get_test_filenames(p_id)

        run = runtime.Run_Tests(c_id, program_file, src_path, tests_path, test_file_names)
        test_run_status = run.run_tests()
        test_run_status = ' '.join(test_run_status)

        conn.send(test_run_status.encode())
        conn.close()


    conn, addr = server.accept()
    received_message = conn.recv(port).decode()
    service_thread = threading.Thread(target=service, args=(conn, addr, received_message))
    service_thread.start()