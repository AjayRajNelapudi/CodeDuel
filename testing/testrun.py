import threading
from subprocess import run

def send_requests(c_id):
    status = run(['python3', 'client.py', c_id, 'SumOfN.c'],
                 cwd='/users/ajayraj/documents/codeduel/client')
    return status.returncode

for i in range(10):
    c_id = str(i % 4 + 1)
    req = threading.Thread(target=send_requests, args=(c_id))
    req.start()
    req.join()
