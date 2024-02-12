
import os, time, sys
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT_NUMBER = 4456
SERVER_ADDR = (IP, PORT_NUMBER)
SIZE = 1024
ENCODE_TYPE = "utf-8"
END_SIGNAL = '**=EOFX=**'
def process_client_request(connectionClient, addr):
    print(f"[NEW SOCKET] {addr} connected.")
    connectionClient.send("GOOD@Welcome to the File Server.".encode(ENCODE_TYPE))
    filePrefix = "new"
    while True:
        data = connectionClient.recv(SIZE).decode(ENCODE_TYPE)
        data = data.split("@")
        cmd = data[0]

        if cmd == "upload":
            data = connectionClient.recv(SIZE)
            data = data.decode()
            if data.endswith(END_SIGNAL):
                x = str(data).split()
                fileLen = str(x[1])
                fileName = str(" ".join(x[2:-1]))
                print("-- Receive file: " + fileName + " (" + fileLen + ")")
                fileName = filePrefix + fileName.capitalize()
                fileHandle = open(fileName, mode='wb')
                #get file (block and save)
                while True:
                    receiveData = connectionClient.recv(SIZE)
                    try: 
                        isEnd = receiveData.decode().endswith(END_SIGNAL)
                        if isEnd == True:
                            break
                    except Exception as execptionOfSending: 
                        print ("Some error is occured on uploading file: \n Content = ")
                        print (str(execptionOfSending))
                    fileHandle.write(receiveData)
                fileHandle.close()
                
                if fileLen == str(os.path.getsize(fileName)): print(">> Size verified.")
                else: print("!! Size mismatch.")
                send_data = "GOOD@File upload successfully."
                connectionClient.send(send_data.encode(ENCODE_TYPE))

        elif cmd == "get":
            print(*data)
            data = connectionClient.recv(SIZE)
            data = data.decode()
            if data.endswith(END_SIGNAL):
                x = str(data).split()
                fileName = str(x[1])
                print("-- Request file: " + fileName)
                try:
                    flen = str(os.path.getsize(fileName))
                except Exception as execptionOfFile:
                    print("File Error. \n content = ")
                    print(str(execptionOfFile))
                    continue
                fstr = 'FILE: ' + flen + ' ' + fileName + ' ' + END_SIGNAL
                print("- Send file: " + fileName + " (" + flen + ")")
                connectionClient.send(fstr.encode())
                time.sleep(1)
                try:
                    with open(fileName, 'rb') as f:
                        fileData = f.read()
                        # Begin sending file
                        connectionClient.sendall(fileData)
                        time.sleep(4)
                        connectionClient.send(END_SIGNAL.encode())
                    f.close()
                    print('>> Transfer: ' + fileName + ' complete.\n')
                except:
                    print('>> Error sending file: ' + fileName + '.\n')
                send_data = "GOOD@File download successfully."
                connectionClient.send(send_data.encode(ENCODE_TYPE))
    print(f"Client will be disconnected.\n")
    connectionClient.close()

def main():
    print("[SERVER REPORT] Server is running")

    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.bind(SERVER_ADDR)
    server_connection.listen()

    print("[SERVER REPORT] Server is listening on")
    print("IP : " +  str(IP) + " PORT Number : " + str(PORT_NUMBER) + "\n")

    while True:
        aceeptedConnection, accpetedAddr = server_connection.accept()
        thread_info = (aceeptedConnection, accpetedAddr)
        print("[SERVER REPORT] client is accepted on ")
        print(str(accpetedAddr) + "\n")

        thread_client = threading.Thread(target=process_client_request, args=thread_info)
        thread_client.start()


if __name__ == "__main__":
    main()
