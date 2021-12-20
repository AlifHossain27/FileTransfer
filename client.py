import socket
import json
from simple_term_menu import TerminalMenu

IP = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 4069


# Receiving Response From The Server
def recvResp(conn):
    rawData=conn.recv(SIZE).decode(FORMAT)
    jsonData=json.loads(rawData)
    if jsonData['Type'] == 'Send':
        return jsonData['Response']

    elif jsonData['Type'] == 'Fetch':
        file=jsonData['File']
        data=jsonData['Data']

        with open(file, "w") as f:
            f.write(data)
        return 'File Downloaded'
    
    
# Disconnecting From The Server
def Exit(conn):
    sendData={
        'Type':'Exit'
        }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT))
    return True
    

# Uploading File To The Server
def uploadFile(path,conn):
    try:
        with open(path,'r') as f:
            uploadData=f.read()

        sendData={
            'Type':'Upload',
            'Path':path,
            'Data':uploadData
        }
        data = json.dumps(sendData)
        conn.sendall(bytes(data,encoding=FORMAT))
        print(recvResp(conn))
        
    except Exception as e:
        print(e)
        pass


# Downloading File From The Server
def downloadFile(path,conn):
    sendData={
        'Type':'Download',
        'File':path
        }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT))
    print(recvResp(conn))
    

# Viewing List of Files In The Server
def Dir(conn):
    sendData={
        'Type':'List'
        }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT)) 
    print(recvResp(conn))   


# Removing Files From The Server
def rmvFile(path,password,conn):
    sendData={
        'Type':'Delete',
        'Path':path,
        'Key':password
        }
    data = json.dumps(sendData)
    conn.sendall(bytes(data,encoding=FORMAT))
    print(recvResp(conn)) 


# Connecting to thr Server
def Client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        print(recvResp(client))
        
        options=['Upload File','Download File','List','Delete File','Exit']
        Menu= TerminalMenu(options)
        quit=False

        while quit == False:
            optionsIndex=Menu.show()
            optionsChoice=options[optionsIndex]

            if optionsChoice=='Exit':
                Exit(client)
                quit = True

            elif optionsChoice =='Upload File':
                filePath=input('Enter File Name/Path: ')
                uploadFile(filePath,client)
                
                
            elif optionsChoice == 'Download File':
                filePath=input('Enter File Name: ')
                downloadFile(filePath,client)
                
            elif optionsChoice == 'List':
                Dir(client)
                
            elif optionsChoice == 'Delete File':
                filePath=input('Enter File Name: ')
                password=input('Enter The Server Password: ')
                rmvFile(filePath,password,client)  

        if quit==True:
            break

    print("Disconnected from the server.")
    client.close()


# Executing The Client Function
if __name__ == "__main__":
    Client()