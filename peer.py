#! /usr/bin/env python

import socket
import sys
import time
import threading
from Vesper import client as cl
import json 

class Server(threading.Thread):
    def __init__(self, usrname):
        threading.Thread.__init__(self)
        self.username = usrname

    def run(self):
        addr = "http://127.0.0.1:5000"
        key = "online"
        #packet = json.loads(str(cl.get(addr, key)))
        packet = cl.get(addr, key)
        res = {}
        if packet['code'] == 'success':
            res = json.loads(packet['payload']['value'])
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Server started successfully\n")
        hostname=''
        #port = socket.SOCK_STREAM
        self.sock.bind((hostname,0))
        self.sock.listen(1)
        res[self.username] = self.sock.getsockname()[1]
        res_str = json.dumps(res)
        cl.put(addr, key, str(res_str))
        print("Listening on port ", self.sock.getsockname()[1])        
        #time.sleep(2)    
        (clientname,address)=self.sock.accept()
        print("Connection from %s\n" % str(address))        
        while 1:
            chunk=clientname.recv(4096)            
            print(str(address)+':'+str(chunk))

class Client(threading.Thread):    
    def connect(self,host,port):
        self.sock.connect((host,port))
    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        print("Sent\n")
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            host=input("Enter the hostname\n>>")            
            port=int(input("Enter the port\n>>"))
        except EOFError:
            print("Error")
            return 1
        
        print("Connecting\n")
        s=''
        self.connect(host,port)
        print("Connected\n")
        while 1:            
            print("Waiting for message\n")
            msg=input('>>')
            if msg=='exit':
                break
            if msg=='':
                continue
            print("Sending\n")
            self.client(host,port,str.encode(msg))
        return(1)


if __name__=='__main__':
    usrname = input("Enter your username: ")
    srv=Server(usrname)
    srv.daemon=True
    print("Starting server")
    srv.start()
    time.sleep(1)
    print("Starting client")
    cli=Client()
    print("Started successfully")
    cli.start()
    
    
