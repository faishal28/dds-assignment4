#! /usr/bin/env python

import socket
import sys
import time
import threading
from Vesper import client as cl
import json 

#configuration objects
f=open('Vesper/ip_list.txt','r')
addrList = f.readlines()
key = "online"

#get available registry server
def getRegServer(flag=0):
        packet={}
        for ip in addrList:
            packet = cl.get(ip, key)
            if isinstance(packet,dict):
                addr=ip
                return (addr,packet)
            else:
                if not flag:
                    print(ip+" Registry server is down.Trying for next registry server\n")
        
        return ("No_server",0)


'''
    Thread class for handling a client connection 
'''
class ClientHandle(threading.Thread):
    def __init__(self, clientname,address):
        threading.Thread.__init__(self)
        self.clientname=clientname
        self.address=address

    #get chat from client in a loop
    def run(self):

        print("\nConnection from %s" % str(self.address))
        while 1:
            chunk=self.clientname.recv(4096).decode()            
            print(str(self.address)+','+chunk)
            if(chunk=="exit"):
                self.clientname.close()
                break
        self.clientname.close()        


'''
Thread class for server daemon
'''
class Server(threading.Thread):
    def __init__(self, usrname):
        threading.Thread.__init__(self)
        self.username = usrname

    

    def run(self):
        #packet = json.loads(str(cl.get(addr, key)))
        
        (addr,packet)=getRegServer()
        if(addr=="No_server"):
            print("\nNo registry servers available")
            return 
                         
                             
        print("\nSelected registry server "+addr)
        res = {}
        if packet['code'] == 'success':
            res = json.loads(packet['payload']['value'])
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("\nServer started successfully\n")
        hostname=''
        #port = socket.SOCK_STREAM
        self.sock.bind((hostname,0))
        self.sock.listen(10)
        res[self.username] = self.sock.getsockname()[1]
        res_str = json.dumps(res)
        cl.put(addr, key, str(res_str))
        print("\nListening on port ", self.sock.getsockname()[1])        
        #time.sleep(2)

        threads=[]

        #listen for client connection in a loop and start a thread for that
        while True:    
            (clientname,address)=self.sock.accept()
            newThread=ClientHandle(clientname,address)
            newThread.start()
            threads.append(newThread)

        for t in threads:
            t.join()
                
'''
Thread class for client creation
'''
class Client(threading.Thread):
    def __init__(self, usrname):
        threading.Thread.__init__(self)
        self.username = usrname

    def connect(self,host,port):
        self.sock.connect((host,port))

    def client(self,host,port,msg):               
        sent=self.sock.send(msg)           
        print("Sent\n")

    def getonline(self):
        (addr,packet)=getRegServer(1)
        if addr=="No_server":
            return addr
        return json.loads(cl.get(addr, key)['payload']['value'])

    def checkonline(self):
        online_users = self.getonline()
        if online_users=="No_server":
            return online_users
        print("\nFollowing are the users online:")
        for key in online_users:
            print(key)
        return online_users

    #connect to user entered
    def connectToUser(self, online_users):
        username=input("Enter the username you want to connect to: ")            
        print("Connecting\n")
        print(online_users)
        self.connect('127.0.0.1',online_users[username])
        print("Connected\n")
        while 1:            
            print("Waiting for message\n")
            msg=input('>>')
            if msg=='exit':
                self.client('127.0.0.1',online_users[username],str.encode(msg))
                break
            if msg=='':
                continue
            print("Sending\n")
            msg=self.username+": "+ msg
            self.client('127.0.0.1',online_users[username],str.encode(msg))

    #disconnect user from system
    def disconnect(self):
        (addr,packet)=getRegServer(1)
        packet = cl.get(addr, key)
        res = {}
        if packet['code'] == 'success':
            res = json.loads(packet['payload']['value'])
        del res[self.username]
        res_str = json.dumps(res)
        cl.put(addr, key, str(res_str))


    def menu(self):
        print("\n1. Check online users")
        print("2. Connect to a user")
        print("3. Disconnect from the network")

    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        #show menu for client
        while(1):
            self.menu()
            choice = int(input("Enter your Choice: "))
            if(choice == 1):
                online_users = self.checkonline()
                if online_users=="No_server":
                    print("\nRegistry servers not available")
            elif(choice == 2):
                online_users = self.getonline()
                if online_users=="No_server":
                    print("\nRegistry servers not available")
                    continue    
                self.connectToUser(online_users)
            else:
                self.disconnect()
                break
        return(1)



if __name__=='__main__':
    usrname = input("Enter your username: ")
    srv=Server(usrname)
    srv.daemon=True
    print("Starting server")
    srv.start()
    time.sleep(2)
    print("Starting client")
    cli=Client(usrname)
    cli.start()
    f.close()
    
    
