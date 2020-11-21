# Peer to Peer Distributed Chat App

This project is done as part of course Distributed Data Systems Course.It involves creating a simple distributed peer to peer system.


## Steps to run app

1. First start the registry servers
```
cd Vesper
python3 server.py 0 ip_list.txt
python3 server.py 1 ip_list.txt
python3 server.py 2 ip_list.txt
python3 server.py 3 ip_list.txt
python3 server.py 4 ip_list.txt
 
```
2. Start the peer process
```
cd ..
python3 peer.py
```

&nbsp;&nbsp;  Any no of peers can be started by running above in different terminals.

