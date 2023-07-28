import socket
from time import sleep

class SocketConnection:
  def __init__(self):
    self.connected = False
    self.client = None
    self.hasConfig = False

  def setConfig(self, config, model, host, port):
    self.timeout = float(config[model]['timeout'])
    self.blocking = int(config[model]['blocking'])
    self.host = host
    self.port = port
    self.hasConfig = True

  def connect(self):
    if not self.hasConfig:
      print("[SocketConnection] Can't connect: no socket configuration provided. Use setConfig(config, model, host, port).")
      return
    self.client = socket.socket()
    self.client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    self.client.settimeout(self.timeout)
    while not self.connected:
      try:
        self.client.connect((self.host, self.port))
        self.client.setblocking(self.blocking==1)
        self.connected = True
        print("[SocketConnection] Connection Successfull")
      except socket.error:
        print("[SocketConnection] Connection failed, sleeping 2 seconds...")
        sleep(2)
    sleep(3)

  def send(self, data, term=''):
    try:
      if self.client is not None and self.connected:
        self.client.send(data)
        return True
      else:
        print("[SocketConnection] Can't send data: Client is None or it's not connected")
        return False
    except ConnectionResetError:
    #except Exception as e:
      self.connected = False
      print(f"[ConnectionResetError] socket send error ")
      self.connect()
      return False

  def read(self):
    try:
      if self.client is not None and self.connected:
        #MATTEO return self.client.recv(8192).decode("UTF-8")
        return self.client.recv(8192)
      else:
        print("[SocketConnection] Can't read data: client is None or it's not connected")
        return False
    except ConnectionResetError:
        self.connected = False
        print(f"[ConnectionResetError] socket receive error")
        self.connect()
        return False
        
  def stop(self):
    if self.client is not None and self.connected:
      self.client.close()
      self.connected = False
      print("[SocketConnection] Connection closed")
    else:
      print("[SocketConnection] Can't close connection: client is None or it's not connected")

