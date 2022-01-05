# 5.
import subprocess
import chardet


ping_google = ['ping', 'google.com']
ping_yandex = ['ping', 'yandex.ru']

def ping_site(data):
  subproc_ping = subprocess.Popen(data, stdout=subprocess.PIPE)
  counter = 0
  for line in subproc_ping.stdout:
    coding = chardet.detect(line)
    if counter < 5:
      line = line.decode(coding['encoding']).encode('utf-8')
      print(line.decode('utf-8'))
      counter += 1
  
    
ping_site(ping_google)


