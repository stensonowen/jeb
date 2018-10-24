
from app import app
from flask import render_template, request, redirect

import requests
from datetime import datetime

import api

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/api/<cmd>', methods=['POST'])
def api_handle(cmd):
    cmd = cmd.strip().split(" ")[0] # for now discard tail
    err = lambda: print("Unknown command '{}'".format(cmd))
    (api.COMMANDS.get(cmd) or err)()
    return "ack"

@app.route('/license')
def get_license():
    return redirect("https://www.gnu.org/licenses/agpl-3.0.en.html", code=302)

@app.route('/ip')
@app.route('/status')
def report_ips():
    return "long live jeb" + "<br><br>" + check_ips()

def get_ip(addr):
    resp = requests.get(addr)
    if resp.ok:
        return resp.text
    else:
        return "Failure: " + resp.reason

def check_ips():
    jebcam = get_ip("https://icanhazip.com")
    deluge = get_ip("http://192.168.0.9:8118")  # piaracy vm
    dt = datetime.now()
    template = '''
    Current IP:  {}<br>
    Torrent IP:  {}<br>
    Page served:  {}<br>
    '''
    return template.format(jebcam, deluge, dt)

#@jeb.route('/status')
#def get_status():
#    status = {'playing': False}
#    return render_template('status.html', date=datetime.now(), ip='123', status=status)



