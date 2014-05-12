import NetworkBuffer
import thread
import threading
from threading import Thread
from NetworkBuffer import NetworkBuffer
import time
import socket

class NetworkInterface(Thread):
    def __init__(self, InputBuffer, OutputBuffer):
        self._InputBuffer = InputBuffer
        self._OutputBuffer = OutputBuffer
        self._Exit = False

    def run(self):
        print "Acceptiong connections \n"
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serverSocket.bind(('', 1337))
        serverSocket.listen(1)
        ConnectedCount = 0

        while self._Exit == False & ConnectedCount == 0:
            clientSocket, address = serverSocket.accept()
            print "Connected with " + address[0] + ":" + str(address[1]) + "\n"
            ConnectedCount += 1
            
            try:
                t =  threading.Thread(target=self.Listen, args = (clientSocket,))
                t2 =  threading.Thread(target=self.Send, args = (clientSocket,))
                t.start()
                t2.start()
            
            except:
                print "Error: Unable to start thread \n"

            time.sleep(1)

    def Listen(self, clientSocket):
        while self._Exit == False:
            data = clientSocket.recv(1024) #buffergroote
            self._InputBuffer.Append(data)  
            time.sleep(1)

    def Send(self, clientSocket):
        data = ""
        while self._Exit == False:
            data = self._OutputBuffer.Pop()
            
            if len(str(data)) > 0:
                print str(data)  
                print "Sending " + data + "\n"
                clientSocket.send(str(data))
                data = ""
        time.sleep(1)

    def Exit(self):
        self._Exit = True
        
            

    

        
        

    
            
