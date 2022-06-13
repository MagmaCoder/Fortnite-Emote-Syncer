import threading
import socket
from datetime import datetime
import os

HOST = "localhost"
PORT = 65432

allowConnections = True

clients = {}

def Client(clientsocket : socket.socket,addr):
    global clients

    clientsocket.setblocking(0)

    while allowConnections:
        pass

def openSocket(host, port):
    conns = {}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        
        s.listen()
        
        while allowConnections:
            conn, addr = s.accept()
            conns[addr] = threading.Thread(target=Client,args=(conn, addr))
            conns[addr].start()

if __name__ == "__main__":
    print(f"Server starting on {HOST} : {PORT}")

    acceptingThread = threading.Thread(target=openSocket,args=(HOST, PORT))
    acceptingThread.start()




