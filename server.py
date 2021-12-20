import os
import socket
import json
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDR = (IP, PORT)
SIZE = 4069
FORMAT = "utf-8"
SERVER_DATA_PATH = "ServerFiles"
PASSWORD = "admin"


# Connection Response
def response(conn, addr):
    sendData = {'Type': 'Send', 'Response': 'Connected to the Server'}
    data = json.dumps(sendData)
    conn.sendall(bytes(data, encoding=FORMAT))


# Uploading File
def Upload(resp, conn):
    path=resp['Path']
    data=resp['Data']
    filepath = os.path.join(SERVER_DATA_PATH, path)

    with open(filepath, "w") as f:
        f.write(data)
    sendData = {
        'Type':'Send',
        'Response':'File Uploaded'
        }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT))


# Downloading File
def Download(resp,conn):
    file=resp['File']
    files = os.listdir(SERVER_DATA_PATH)

    if file in files:
        filepath=f'{SERVER_DATA_PATH}/{file}'

        with open(filepath, "r") as f:
            download_data = f.read()
        
        sendData = {
                'Type':'Fetch',
                'File':file,
                'Data':download_data
                }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))
    
    else:
        sendData = {
            'Type':'Send',
            'Response':'File not found'
            }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))


# Server Files List
def Dir(conn):
    files = os.listdir(SERVER_DATA_PATH)
    file_list=[]
    if len(files) == 0:
        sendData = {
        'Type':'Send',
        'Response':'The Server is Empty'
        }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))
    else:
        for f in files:
            file_list.append(f)
        
        sendData = {
        'Type':'Send',
        'Response':file_list
        }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))


# Remove File From The Server
def rmvFile(resp,conn):
    if resp['Key'] != PASSWORD:
        sendData = {
        'Type':'Send',
        'Response':'Wrong Password'
        }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))
    else:
        files = os.listdir(SERVER_DATA_PATH)
        file=resp['Path']
        if len(files) == 0:
            sendData = {
            'Type':'Send',
            'Response':'The Server is Empty'
            }
            data = json.dumps(sendData)
            conn.sendall(bytes(data,encoding=FORMAT))
        else:
            if file in files:
                os.system(f"rm {SERVER_DATA_PATH}/{file}")
                sendData = {
                'Type':'Send',
                'Response':'File deleted'
                }
                data = json.dumps(sendData)
                conn.sendall(bytes(data,encoding=FORMAT))
            else:
                sendData = {
                'Type':'Send',
                'Response':'File not found'
                }
                data = json.dumps(sendData)
                conn.sendall(bytes(data,encoding=FORMAT))


# Handling Connections
def handleClient(conn, addr):
    print(f"[CONNECTION] {addr} connected.")
    response(conn, addr)
    while True:
        rawData = conn.recv(SIZE).decode(FORMAT)
        jsonData = json.loads(rawData)

        if jsonData['Type'] == 'Exit':
            break

        elif jsonData['Type'] == 'Upload':
            Upload(jsonData, conn)

        elif jsonData['Type'] == 'Download':
            Download(jsonData, conn)
        
        elif jsonData['Type'] == 'List':
            Dir(conn)
        
        elif jsonData['Type'] == 'Delete':
            print(jsonData)
            rmvFile(jsonData,conn)

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


# Running The Server
def Server():
    print("[STARTING ...]")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING ...] {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


# Executing The Server Function
if __name__ == "__main__":
    Server()
