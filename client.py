# My chat room client. Version Two
# student name: Weiliang Xia
# srudent id: 14281543
# data 12/3/2017
# description:
# In this project, I extend version 1 by using threads to implement a chat room that includes multiple clients and a server that utilizes the socket API.
# The client program provides commands: login (allow users to join the chat room), send (unicast or broadcast a message; actually send the message to the server and the server forwards the message), logout (quit the chat room), and who (list all the clients in the chat room).
# The server runs a chat room service, manages all the clients and distributes the messages.


import socket
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 11543))
print('My chat room client. Version Two ')
print('please signup or login first')
verif = raw_input()
print(verif)
sock.send(verif.encode())

#sock.send(b'1')
print(sock.recv(1024).decode())

#while (sock.recv(1024).decode()!='successfully, welcome to server!'):
 #   print('please try again:  ')
  #  verif = input()
   # sock.send(verif.encode())


message = raw_input()
sock.send(message.encode())


def sendThreadFunc():
    while True:
        try:
            myword = input()
            sock.send(myword.encode())
            # print(sock.recv(1024).decode())
        except Exception:
            print('Server closed this connection!')
        except Exception:
            print('Server is closed!')


def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except Exception:
            print('Server closed this connection!')

        except Exception:
            print('Server is closed!')


th1 = threading.Thread(target=sendThreadFunc)
th2 = threading.Thread(target=recvThreadFunc)
threads = [th1, th2]

for t in threads:
    t.setDaemon(True)
    t.start()
t.join()