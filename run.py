import argparse, pickle, multiprocessing #-
from socket   import *                   #-
from time     import sleep               #-
from random   import *                   #-
from constRPC import *                   #-
#-
from client   import *                   #-
from server   import *                   #-
from dbclient import *                   #-
#-
def client1(server_host=HOSTS, server_port=PORTS, client2_host=HOSTC2,
            client2_port=PORTC2, bind_host=BIND_HOST, client_port=PORTC1,
            start_client2=False):
  c1   = Client(client_port, bind_host)       # create client
  dbC1 = DBClient(server_host, server_port)   # create reference
  dbC1.create()                               # create new list
  dbC1.appendData('Client 1')                 # append some data
  if start_client2: #-
    multiprocessing.Process(target=client2).start() # create 2nd client #-
    sleep(2)                                  # make sure the other client is running #-
  c1.sendTo(client2_host, client2_port, dbC1) # send to other client

def client2(bind_host=BIND_HOST, client_port=PORTC2, stop_server=True):
  c2   = Client(client_port, bind_host)       # create a new client
  data = c2.recvAny()                         # block until data is sent
  dbC2 = pickle.loads(data)                   # receive reference
  dbC2.appendData('Client 2')                 # append data to same list
  print(dbC2.getValue()) #-
  if stop_server: #-
    c2.sendTo(dbC2.host, dbC2.port, [STOP]) #-

def server(bind_host=BIND_HOST, port=PORTS, start_client1=False): #-
  server = Server(port, bind_host) #-
  if start_client1: #-
    multiprocessing.Process(target=client1, kwargs={'start_client2': True}).start() # create 1st client #-
  server.run() #-

def local(): #-
  s = multiprocessing.Process(target=server, kwargs={'start_client1': True}) #-
  s.start() #-
  s.join() #-

def main(): #-
  parser = argparse.ArgumentParser() #-
  parser.add_argument('role', nargs='?', default='local',
                      choices=['local', 'server', 'client1', 'client2']) #-
  parser.add_argument('--bind-host', default=BIND_HOST) #-
  parser.add_argument('--server-host', default=HOSTS) #-
  parser.add_argument('--server-port', type=int, default=PORTS) #-
  parser.add_argument('--client1-port', type=int, default=PORTC1) #-
  parser.add_argument('--client2-host', default=HOSTC2) #-
  parser.add_argument('--client2-port', type=int, default=PORTC2) #-
  parser.add_argument('--keep-server-running', action='store_true') #-
  args = parser.parse_args() #-

  if args.role == 'server': #-
    server(args.bind_host, args.server_port) #-
  elif args.role == 'client1': #-
    client1(args.server_host, args.server_port, args.client2_host,
            args.client2_port, args.bind_host, args.client1_port) #-
  elif args.role == 'client2': #-
    client2(args.bind_host, args.client2_port, not args.keep_server_running) #-
  else: #-
    local() #-

if __name__ == "__main__": #-
  main() #-
