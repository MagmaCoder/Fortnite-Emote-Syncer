import threading
import socket
from datetime import datetime
import os
import uuid

HOST = "localhost"
PORT = 65432

allowConnections = True

clients = {}

def Client(clientsocket : socket.socket,addr):
    global clients

    msg = b""

    clientsocket.setblocking(0)

    while allowConnections:
        if msg != b"":
            pass
        try:
            #10035 is no data
            #10054 is closed connection
            msg = clientsocket.recv(1024)
        except WindowsError as e:
            if e.winerror == 10054:
                print(f"Connection closed.")
                clientsocket.close()
                break
    
    clientsocket.close()

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




