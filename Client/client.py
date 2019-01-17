try:
    from Client import filetransfer
except:
    pass

try:
    import filetransfer
except:
    pass

import sys
import socket

def push_file_to_server(c_id, program_file):
    push_file = filetransfer.FileUpload(c_id)
    push_file.upload_file(program_file)

    server = socket.socket()
    hostname, port = 'localhost', 32757
    server.connect((hostname, port))
    message = str(c_id) + ',' + program_file
    server.send(message.encode())

    test_run_status = server.recv(1024)
    print(test_run_status.decode())

    server.close()

if len(sys.argv) != 3:
    print('Incorrect No of args')
else:
    push_file_to_server(int(sys.argv[1]), sys.argv[2])
