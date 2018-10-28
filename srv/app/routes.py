#!/usr/bin/env python3

from app import app
from flask import render_template, request

import requests
from datetime import datetime

import api

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/api/<cmd>', methods=['POST'])
def api_handle(cmd):
    parts = [p.strip() for p in cmd.split(' ', 1)]
    func = parts[0]     # type: str
    tail = parts[1] if len(parts) == 2 else None
    err = lambda *_: print("Unknown command '{}'".format(cmd))
    (api.COMMANDS.get(func) or err)(tail)
    return "ack"

@app.route('/license')
def get_license():
    url = "https://www.gnu.org/licenses/agpl-3.0.en.html"
    return flask.redirect(url, code=302)

@app.route('/ip')
@app.route('/status')
def report_ips():
    return "long live jeb" + "<br><br>" + check_ips()

def get_ip(addr):
    resp = requests.get(addr)
    return resp.text if resp.ok else "Failure: {}".format(resp.reason)

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



