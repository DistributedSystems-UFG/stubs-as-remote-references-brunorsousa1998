import pickle, os      #-
from socket   import * #-
from constRPC import * #-
#-
class Client:
  def __init__(self, port, host=BIND_HOST):
    self.host = host                    # address to listen on
    self.port = port                    # port it will listen to
    self.sock = socket()                # socket for incoming calls
    self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port)) # bind socket to an address
    self.sock.listen(2)                 # max num connections

  def sendTo(self, host, port, data):
    sock = socket()
    sock.connect((host, port))       # connect to server (blocking call)
    sock.send(pickle.dumps(data))    # send some data
    sock.close()

  def recvAny(self):
    (conn, addr) = self.sock.accept()
    return conn.recv(1024)
