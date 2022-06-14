import threading
import socket
from datetime import datetime
import os
import uuid
import json

def startPacket():
    currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    
    initialPacket = {"type":"start","datetime":currentTime,"uuid":str(uuid.uuid4())}
    return json.dumps(initialPacket).encode("utf-8")

HOST = "localhost"
PORT = 65432

allowConnections = True

clients = {}

def Client(clientsocket : socket.socket,addr):
    global clients

    msg = b""
    print("Connection started.")
    clientsocket.setblocking(0)

    #Send Initial Accept Packet
    
    clientsocket.send(startPacket())


    while allowConnections:
        if msg != b"":
            print(msg)
            msg = b""
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

def OpenSocket(host, port):
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

    acceptingThread = threading.Thread(target=OpenSocket,args=(HOST, PORT))
    acceptingThread.start()






