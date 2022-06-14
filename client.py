import socket
import pynput
import threading
import json
from datetime import datetime

def pingPacket(ping):
    initialPacket = {"type":"ping","datetime":currentTime}
    return json.dumps(initialPacket).encode("utf-8")

def Socket(hostIP, hostPort):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((hostIP, hostPort))
        
        s.setblocking(0)

        msg = b""
        print(f"Connected to {hostIP}.")
        while True:
            try:
                msg = s.recv(1024)
            except WindowsError as e:
                if e.winerror == 10054:
                    print("Closed connection.")
                    return

            if msg != b"":
                try:
                    msg = json.loads(msg.decode("utf-8"))
                    datetimeInterpret = datetime.strptime(msg["datetime"], "%Y-%m-%d %H:%M:%S:%f")
                    ping = datetime.now() - datetimeInterpret
                    print(ping)
                    msg = b""
                except:
                    pass

if __name__ == "__main__":
    mainSocket = threading.Thread(target=Socket,args=("localhost",65432))
    mainSocket.start()