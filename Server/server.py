
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


username = 'ajay'
port = 12345
authorizer = DummyAuthorizer()
authorizer.add_user(username, port, "/users/ajayraj/documents/codeduel", perm="elradfmw")
authorizer.add_anonymous("/users/ajayraj/documents/codeduel", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 1026), handler)
server.serve_forever()