import NetworkBuffer
import thread
import threading
from threading import Thread
from NetworkBuffer import NetworkBuffer
from NetworkClient import NetworkClient
import time
import socket

class NetworkInterface(Thread):
    def __init__(self, Buffer):
        self._NetworkClients = []
        self._Buffer = Buffer
        self._Exit = False
        self._Identify = 1

    def run(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverSocket.bind(('', 1337))
        serverSocket.listen(1)

        while self._Exit == False:
            clientSocket, address = serverSocket.accept()
            networkclient = NetworkClient(clientSocket, self._Identify)
            self._NetworkClients.append(networkclient)
            self._Identify += 1

            print "Connected with " + address[0] + ":" + str(address[1]) + "\n"
            
            try:
                t =  threading.Thread(target=self.Listen, args = (networkclient,))
                t.start()
            
            except:
                print "Error: Unable to start thread \n"

            time.sleep(1)

    def Listen(self, clientSocket):

        while self._Exit == False:

            data = clientSocket.getClientSocket().recv(1024) #buffergroote
            while "<EOF>" not in data:
                data = data + clientSocket.getClientSocket().recv(1024)

            data = data[:data.find("<EOF>")]
            self._Buffer.Append("<ID" + clientSocket.getClientID() + ">" + data)
            time.sleep(0.100)

    def Send(self, Data, ID):
        print "Data: " + Data + " ID: " + ID
        ID = ID[3:4]

        ClientSocket = 0
        if len(str(Data)) > 0:
            for c in self._NetworkClients:
                if c.getClientID() == ID:
                    ClientSocket = c
                    break

            ClientSocket.getClientSocket().send(str(Data) + "<EOF>")

    def Exit(self):
        self._Exit = True
        
            


        
        




            
