import requests
from uuid import getnode as get_mac
import socket
import time
import os

sleep_time = 5
master_port = '4000'
master_ip = '10.117.119.203'
master_lan_ip = '10.117.108.130'
mac = hex(get_mac())

flag = True
chrome_url = None
attempts = 1

ip_string = os.popen('ip addr show wlan0 | grep inet').read()
ip = ip_string.split()[1].split('/')[0]

print "Hello! My name is pi."
print "My ip address is " + ip + '!'
print "I will now inform my master."


while flag:
    if attempts % 10 == 0:
        request_ip = master_lan_ip
    else:
        request_ip = master_ip
    print('Trying to contact Master Pi on ''...\n')
    request_string = 'http://' + request_ip + ':' + master_port + '/register/' + mac + '?' + 'ip=' + ip
    r = requests.get(request_string)
    response = r.json()
    if r.status_code is 200:
        if 'url' in response:
            print('Url received from master ' + response['url'] + '\n')
            chrome_url = response['url']
            break
    print('Trying again in ' + str(sleep_time) + ' seconds\n')
    time.sleep(sleep_time)

f = open('.xinitrc', 'w+')
f.write('chromium --kiosk --ignore-certificate-errors --disable-restore-session-state --disable-infobars --disable-session-crashed-bubble ' + chrome_url)



