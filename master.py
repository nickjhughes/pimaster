from flask import Flask, request, jsonify
import json
import cPickle as pickle
import os
import datetime

app = Flask(__name__)

app.config['STORAGE_FILE'] = "clients.db"

def load_db():
    if os.path.isfile(app.config['STORAGE_FILE']):
        return pickle.load(open(app.config['STORAGE_FILE'], "rW"))
    return {}

def save_db(db):
    pickle.dump(db, open(app.config['STORAGE_FILE'], "wb"))
    return True


@app.route('/clients')
def clients():
    clients = load_db()
    return jsonify(clients)

@app.route('/register/<client_id>')
def register(client_id):
    clients = load_db()
    
    if client_id not in clients:
        clients[client_id] = {'mac_address': client_id}

    clients[client_id]['ip_address'] = request.args.get('ip')
    clients[client_id]['last_time'] = datetime.datetime.now()

    save_db(clients)

    print ""
    print clients[client_id]
    print ""

    return jsonify(clients[client_id])


@app.route('/update-url/<client_id>')
def update(client_id):
    clients = load_db()

    clients[client_id]['url'] = request.args.get('url')

    return jsonify({'success': save_db(clients)})



@app.route('/init')
def init():
    server_addr = "http://10.117.119.203:4000"

    return """#!/bin/bash
#dont ever remove this line
echo "curl -s """ + server_addr + """/init | bash" | sudo tee /etc/rc.local > /dev/null

sudo su pi
cd ~/


curl -s """ + server_addr + """/static/boot.py > boot.py
rm -rf .ssh/
mkdir .ssh/
curl -s """ + server_addr + """/static/ssh_keys > .ssh/authorized_keys
curl -s """ + server_addr + """/static/chrome_prefs > .config/chromium/Default/Preferences

curl -s """ + server_addr + """/static/ping.py > ping.py
curl -s """ + server_addr + """/static/crontab > crontab.txt
crontab crontab.txt

sudo pip install requests
sudo rm .xinitrc

python boot.py

startx
"""



if __name__ == "__main__":
    app.run(port=4000, debug=True, host="0.0.0.0")
