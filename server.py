import os
import socket
import json
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 7060
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "ServerFiles"


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    sendData = {
                'Type':'Send',
                'Response':'Connected to the Server'
                }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT))


    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        jsonData=json.loads(data)
        

        if jsonData['Type'] == 'Exit':
           break
        
        if jsonData['Type'] == 'Upload':
            path=jsonData['Path']
            uploadData=jsonData['Data']

            filepath = os.path.join(SERVER_DATA_PATH, path)
            with open(filepath, "w") as f:
                f.write(uploadData)
            sendData = {
                'Type':'Send',
                'Response':'File Uploaded'
                }
            data = json.dumps(sendData)
            conn.sendall(bytes(data,encoding=FORMAT))
        
        if jsonData['Type'] == 'List':
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

        if jsonData['Type'] == 'Delete':
            files = os.listdir(SERVER_DATA_PATH)
            file=jsonData['Path']

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

        if jsonData['Type'] == 'Download':
            file=jsonData['Path']
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


    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


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

if __name__ == "__main__":
    Server()