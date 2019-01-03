
import socket
import threading
import re
import copy
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MAXUSER = 3

sock.bind(('localhost', 11543))

sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')

mydict = dict()
mylist = list()


# pass whatToSay to everybody except the sender
def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass


def tellone(ToName, whatToSay):
    for c in mylist:
        x=c.fileno()
        if mydict[x] == ToName:
            try:
                c.send(whatToSay.encode())
            except:
                pass

def who(hisnumber, message):
    for c in mylist:
        if c.fileno() == hisnumber:
            try:
               c.send(message.encode())
            except:
               pass




def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print(nickname, 'login')
    tellOthers(connNumber, ' System: ' + mydict[connNumber] + ' entered the chatroom')

    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()

            f = lambda recvedMsg: [e.lower() for e in re.findall(r'\b\w+\b', recvedMsg)]
            a = f(recvedMsg)
            b = copy.deepcopy(a)

            b.remove(b[0])

            str1 = ' '.join(b)

         #   print(str2)




         #   if a[0]=='login':
          #      print('#login()')

            if a[0]== 'sendall':
                print(mydict[connNumber], ':', str1)
                tellOthers(connNumber, mydict[connNumber] + ' :' + str1)

            elif a[0]== 'send':
                c = copy.deepcopy(a)
                c.remove(c[0])
                c.remove(c[0])
                str2 = ' '.join(c)
                print(mydict[connNumber], '( to', a[1], '):', str2)
                tellone(a[1], mydict[connNumber] + ' :' + str2)

            elif a[0] == 'who':
                #print('who')
                str3 = str(mydict)
                who(connNumber, str3)


            elif a[0] == 'logout':
                #print('logout')
                try:
                    mylist.remove(myconnection)
                except:
                    pass
                print(mydict[connNumber], 'logout, ', len(mylist), ' person left')
                tellOthers(connNumber, 'System: ' + mydict[connNumber] + ' left')

                myconnection.close()
                return
            else:
                who(connNumber, 'please re-enter the command from the following choice: sendall send who logout')







        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
            tellOthers(connNumber, ' System: ' + mydict[connNumber] + ' left the chatroom')

            myconnection.close()
            return










n=4

while True:
    connection, addr = sock.accept()
    # create a new thread for this connection
    mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
    mythread.setDaemon(True)
    mythread.start()
    #print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        buf = connection.recv(1024).decode()
        #print(buf)

        v = buf.split(' ')
        if v[0]=='login':
            #print('login')
            f = open('user')
            lines=f.readlines()
            for line in lines:
                n = line.split(' ')
                #print(n)



                if (v[1]==n[0] and v[2]==n[1]) or (v[1]==n[0] and v[2]+'\n'==n[1]):
                    #print(v)
                    connection.send(b'successfully, welcome to server!,please enter your name: ')

                    # create a new thread for this connection
                    mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
                    mythread.setDaemon(True)
                    mythread.start()
                # count = count +1
            else:
                connection.send(b'wrong, please re-open the client and try again with correct password')


        elif v[0]=='signup':
            writable = 1
            f = open('user')
            lines=f.readlines()
            for line in lines:
                n = line.split(' ')



                if (v[1] == n[0]):
                    connection.send(b'wrong, user id exits, please re-open the client and try again')
                    writable=0

            if writable==1:
                f = open('user', 'a+')
                f.write('\n' + v[1]+' '+v[2])
                f.close()
                connection.send(b'successfully, welcome to server!,please enter your name: ')

            # count = count +1



        else:
            connection.send(b'wrong, please re-open the client and try again with login or signup')
           # connection.close()
    except:
        pass
