import socket
import json
from simple_term_menu import TerminalMenu


IP = socket.gethostbyname(socket.gethostname())
PORT = 7060
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024


def Client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)

        options=['Upload File','Download File','List','Delete File','Exit']
        Menu= TerminalMenu(options)
        quit=False

        while quit == False:
            jsonData=json.loads(data)

            if jsonData['Type'] == 'Send':
                print(jsonData['Response'])
                

            elif jsonData['Type'] == 'Fetch':
                file=jsonData['File']
                data=jsonData['Data']

                with open(file, "w") as f:
                    f.write(data)
                print("File downloaded")


            optionsIndex=Menu.show()
            optionsChoice=options[optionsIndex]
            if optionsChoice=='Exit':
                sendData={'Type':'Exit'}
                data = json.dumps(sendData)
                client.sendall(bytes(data,encoding=FORMAT))
                quit=True
            
            elif optionsChoice =='Upload File':
                filePath=input('Enter File Name/Path: ')
                try:
                    with open(filePath,'r') as f:
                        uploadData=f.read()

                    sendData={
                        'Type':'Upload',
                        'Path':filePath,
                        'Data':uploadData
                    }
                    data = json.dumps(sendData)
                    client.sendall(bytes(data,encoding=FORMAT))
                    break
                except:
                    print('File not found')
                    pass
                
                
            
            elif optionsChoice == 'List':
                sendData={
                    'Type':'List'
                    }
                data = json.dumps(sendData)
                client.sendall(bytes(data,encoding=FORMAT))
                break
            
            elif optionsChoice == 'Delete File':
                filePath=input('Enter File Name: ')
                password=input('Enter The Server Password: ')
                sendData={
                    'Type':'Delete',
                    'Path':filePath,
                    'Key':password
                    }
                data = json.dumps(sendData)
                client.sendall(bytes(data,encoding=FORMAT))
                break
            
            elif optionsChoice == 'Download File':
                filePath=input('Enter File Name: ')
                sendData={
                    'Type':'Download',
                    'Path':filePath
                    }
                data = json.dumps(sendData)
                client.sendall(bytes(data,encoding=FORMAT))
                break
        
        if quit==True:
            break
        
        

        
    print("Disconnected from the server.")
    client.close()
            
    


if __name__ == "__main__":
    Client()