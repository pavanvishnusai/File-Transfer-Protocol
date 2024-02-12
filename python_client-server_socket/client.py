import socket
import os
import time
import sys
FORMAT = "utf-8"

SERVER = "127.0.0.1"
#PORT = 5550
PORT = int(sys.argv[1])
ADDRESS = (SERVER, PORT)

HEADER_SIZE = 1024 #bits accepted in the first message the client sends
            #adjust in case your server needs a longer length

DISCONNECT = "CLOSE"
UPLOAD_FILE = "upload"
GET_FILE = "get"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)
def uploadFile(file_name):
    msg = f"FILENAME:{file_name}"
    print(f"[CLIENT] Sending file name: {file_name}")
    client.send(msg.encode(FORMAT))
    """ Send the data """
    try:
        with open(os.path.join(file_name), 'rb') as f:
            fileData = f.read()
            # Begin sending file
            client.sendall(fileData)
            time.sleep(4)
            client.send('=FINISH='.encode())
        f.close()
    except Exception as e:
        print("File Sending Error : " + str(e))
    msg = client.recv(HEADER_SIZE).decode(FORMAT)
    print(f"[CLIENT] Uploading Successfuly")

def getFile(file_name):
    msg = f"FILENAME:{file_name}"
    print(f"[CLIENT] Sending file name: {file_name}")
    client.send(msg.encode(FORMAT))

    """ Recv data from client """
    print(f"[CLIENT] Receiving the file from Server.")
    file_path = os.path.join("new" + file_name.capitalize())
    file = open(file_path, "wb")
    while True:
        msg = client.recv(1024)
        try: 
            if msg.decode().endswith('=FINISH=') == True: break
        except: pass
        file.write(msg)
    file.close()
    client.send("File data received".encode(FORMAT))
    print("File is Dwonloaded correctly. \n")

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER_SIZE - len(sendLength))
    client.send(sendLength)
    client.send(message)

while True:
    userCmd = input("Input command:\n>>")
    userCmd = userCmd.split(" ")
    command = userCmd[0]
    if command == DISCONNECT:
        send(command)
        client.close()
    if command == UPLOAD_FILE:
        send(command)
        uploadFile(userCmd[1])
    if command == GET_FILE:
        send(command)
        getFile(userCmd[1])