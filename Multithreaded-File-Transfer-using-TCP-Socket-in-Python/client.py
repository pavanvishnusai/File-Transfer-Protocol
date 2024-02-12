import socket,time,os,sys

IP = socket.gethostbyname(socket.gethostname())
SIZE = 1024
END_SIGNAL = '**=EOFX=**'
ENCODE_TYPE = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = int(sys.argv[1])
    ADDR = (IP, PORT)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(ENCODE_TYPE)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "GOOD":
            print(f"{msg}")

        data = input("> ")
        data = data.split(" ")
        cmd = data[0]

        if cmd == "upload":
            #send upload signal to server
            send_data = f"{cmd}@{cmd}@{cmd}"
            client.send(send_data.encode(ENCODE_TYPE))
            file = data[1]
            try:
                flen = str(os.path.getsize(file))
            except:
                print("No Such file error")
                continue
            fstr = 'FILE: ' + flen + ' ' + os.path.basename(file) + ' ' + END_SIGNAL
            print("- Send file: " + os.path.basename(file) + " (" + flen + ")")
            client.send(fstr.encode())
            time.sleep(1)
            try:
                with open(file, 'rb') as f:
                    fileData = f.read()
                    # Begin sending file
                    client.sendall(fileData)
                    time.sleep(4)
                    client.send(END_SIGNAL.encode())
                f.close()
                print('>> Transfer: ' + file + ' complete.\n')
            except:
                print('> Error sending file: ' + file + '.\n')

        elif cmd == "get":
            #send upload signal to server
            send_data = f"{cmd}@{cmd}@{cmd}"
            client.send(send_data.encode(ENCODE_TYPE))
            #send file name to dowonload to server
            file = data[1]
            fstr = 'FILE: ' + file + ' ' + ' ' + END_SIGNAL
            client.send(fstr.encode())
            time.sleep(1)
            data = client.recv(SIZE)
            data = data.decode()
            if data.endswith(END_SIGNAL):
                x = str(data).split()
                fileLen = str(x[1])
                fileName = str(" ".join(x[2:-1]))
                fileName = "new" + fileName.capitalize()
                print("-- Receive file: " + fileName + " (" + fileLen + ")")
                fileHandle = open(fileName, mode='wb')
                while True:
                    receiveData = client.recv(SIZE)
                    try: 
                        isEnd = receiveData.decode().endswith(END_SIGNAL)
                        if isEnd == True:
                            break
                    except Exception as exceptOfDownload: 
                        #print exception log
                        print ("Some error is occured on uploading file: \n Content = ")
                        print (str(exceptOfDownload))
                    fileHandle.write(receiveData)
                fileHandle.close()
                if fileLen == str(os.path.getsize(fileName)): 
                    print(">> File Size is verified. \n")
                else:
                    print("<< File Size is not mismatched. \n")

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
