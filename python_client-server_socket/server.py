import socket
import threading
import os
import time
FORMAT = "utf-8"

server_name = "127.0.0.1"
PORT = 5550

ADDRESS = (server_name,PORT)

HEADER_SIZE = 1024 #bits accepted in the first message the client sends
            #adjust in case your server needs a longer length

UPLOAD_FILE = "upload"
GET_FILE = "get"

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(ADDRESS)
def receiveFile(clientSocket):
    msg = clientSocket.recv(HEADER_SIZE).decode(FORMAT)
    cmd, data = msg.split(":")
    print(f"[CLIENT] Received the filename: {data}.")

    file_path = os.path.join("new" + data.capitalize())
    clientSocket.send("Filename received.".encode(FORMAT))

    """ Recv data from client """
    print(f"[CLIENT] Receiving the file data.")
    file = open(file_path, "wb")
    while True:
        msg = clientSocket.recv(1024)
        try: 
            if msg.decode().endswith('=FINISH=') == True: break
        except: pass
        file.write(msg)
    file.close()
    clientSocket.send("File data received".encode(FORMAT))
    print("File is Uploaded correctly. \n")
def sendFile(clientSocket):
    msg = clientSocket.recv(HEADER_SIZE).decode(FORMAT)
    cmd, data = msg.split(":")
    print(f"[Server] Received the filename: {data}.")

    try:
        with open(os.path.join(data), 'rb') as f:
            fileData = f.read()
            # Begin sending file
            clientSocket.sendall(fileData)
            time.sleep(4)
            clientSocket.send('=FINISH='.encode())
        f.close()
    except Exception as e:
        print("File Sending Error : " + str(e))
    msg = clientSocket.recv(HEADER_SIZE).decode(FORMAT)
    print(f"[Server] Sending File Successfuly")

    pass
def client(conn,addr):
    print(f"NEW CONNECTION: {addr} connected...")
    connected = True
    while connected:
        msgLength = conn.recv(HEADER_SIZE).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == UPLOAD_FILE:
                print(UPLOAD_FILE)
                receiveFile(conn)
            if msg == GET_FILE:
                print(GET_FILE)
                sendFile(conn)
    conn.close()

def start():
    print(f"SERVER IS LISTENING ON {server_name}")
    serverSocket.listen()
    while True:
        conn, addr = serverSocket.accept()
        thread = threading.Thread(target=client, args=(conn,addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.activeCount() - 1}\n")

print(f"SERVER {server_name} IS STARTING, PLEASE WAIT...")
start()
