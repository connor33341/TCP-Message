import socket
import uuid
import http.client
import asyncio
from threading import Thread
#from multiprocessing import Process
"""
    Authors: Connor W (connor33341)
    Purpose: Simple Proof of concept using TCP requests
    Build: 1/14/22
    PythonVersion: 3.11.8
    BuildVersion: 1.2
    Secure: No
"""

"""
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 80))
# become a server socket
serversocket.listen(5)
# accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()
"""
DefaultPort = "8080"
VERSION = ""
with open("latest.txt","r") as Latest:
    VERSION = Latest.readline()
VERSIONATTACH = " (1/14/22 BUILD) (3.11.8 LV) (LISENCE: MIT)"
class MessageServer:
    def __init__(self,Port,LogFile):
        self.Port = Port
        self.Running = True
        self.Hosts = []
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Log = LogFile
    def Bind(self):
        self.Socket.bind((socket.gethostname(),8080))
    def SearchHosts(self,Address):
        for Host in self.Hosts:
            if Host[0] == Address:
                return Host
    def Recive(self):
        self.Socket.listen(5)
        while self.Running:
            (ClientSocket, Address) = self.Socket.accept()
            Message = self.Socket.recv(2048).decode("utf-8")
            Name = Address
            Key = self.SearchHosts(Address)
            if (Key):
                Name = Key[1]
            else:
                Name = input(f"Enter a name for host ${Address}: ")
                #self.Hosts[len(self.Hosts)+1] = [Address,Name]
                self.Hosts.append([Address,Name])
            Accept = input(f"Accept Message from: ${Name}? [YES:NO]: ")
            if (Accept.lower()=="yes"):
                print("Connection Accepted")
                #Message = self.Socket.recv(2048).decode("utf-8")
                print(f"{Name}: {Message}")
                with open(self.Log,"a") as LogFile:
                    LogFile.write(f"[RECV][{Address}:{self.Port}][{Name}]: {Message}\n")
                    LogFile.close()
                if (Message == "$end"):
                    raise RuntimeError("Device recived end cmd")
            else:
                print("Connection Ended")
            ClientSocket.close()
        print("ServerSocket Closed")
        self.Socket.close()
class MessageClient:
    def __init__(self,Port,LogFile):
        self.Port = Port
        self.Running = True
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Log = LogFile
    def Send(self):
        while self.Running:
            try:
                #await asyncio.sleep(4)
                Address = input("Device Address: ") or ""
                Message = input("Message: ")
                self.Socket.connect((Address,self.Port))
                self.Socket.send(Message.encode("utf-8"))
                with open(self.Log,"a") as LogFile:
                    LogFile.write(f"[SENT][{Address}:{self.Port}]: {Message}\n")
                    LogFile.close()
            except Exception as Error:
                print(f"Message Failed: {Error}")
                with open(self.Log,"a") as LogFile:
                    LogFile.write(f"[SEND-ERR][{Address}:{self.Port}]: {Error}\n")
                    LogFile.close()
        print("ClientSocket Closed")
        self.Socket.close()

if __name__ == "__main__":
    print(f"TCP Message System v{VERSION}")
    LogFileName = "logs/"+str(uuid.uuid4())
    print(f"Log File: {LogFileName}")
    LogFile = open(LogFileName,"x")
    LogFile.write(f"[BEGIN][{LogFileName}]: {VERSION}{VERSIONATTACH}\n")
    try:
        print("Running Version Check (May take a minuite)")
        Host = "raw.githubusercontent.com"
        HttpConnection = http.client.HTTPConnection(Host, timeout=60)
        HttpConnection.request("GET","/connor33341/TCP-Message/main/latest.txt", headers={"Host":Host})
        Response = HttpConnection.getresponse()
        ReadResponse = str(Response.read().decode())
        #ReadResponse = b""+Response.read() # Decode bytes
        if (VERSION != ReadResponse):
            print(f"Version out of date, please update at https://github.com/connor33341/TCP-Message/ [{VERSION}<{ReadResponse}]")
            LogFile.write(f"[OUTDATED][{VERSION}][{ReadResponse}]: Please update at https://github.com/connor33341/TCP-Message/")
        else:
            print("Version up to date")    
    except Exception as Error:
        print(f"Version Error: {Error}")
    LogFile.close()
    Port = input("Host Port (Press enter to use default): ")
    Port = Port or DefaultPort
    try:
        Port = int(Port)
    except (ValueError) as ValueErrorMessage:
        print(f"Value Error: {ValueErrorMessage}")
    except (Exception) as Error:
        print(f"Error: {Error}")
    Begin = input("Begin [YES/NO]: ")
    if (Begin.lower() != "yes"):
        raise RuntimeError("Server Ended")
    print(f"Server Started at: {socket.gethostname()}:{Port}")
    MessageServerClass = MessageServer(Port,LogFileName)
    MessageClientClass = MessageClient(Port,LogFileName)
    def ServerHandle():
        print("ServerHandle Begin")
        try:
            MessageServerClass.Bind()
            MessageServerClass.Recive()
        except Exception as Error:
            MessageServerClass.Running = False
            print(f"ServerHandle Error: {Error}")
    def ClientHandle():
        print("ClientHandle Begin")
        try:
            MessageClientClass.Send()
        except Exception as Error:
            MessageClientClass.Running = False
            print(f"ClientHandle Error: {Error}")
    ClientThread = Thread(target=ClientHandle)
    ServerThread = Thread(target=ServerHandle)
    ClientThread.start()
    ServerThread.start()
