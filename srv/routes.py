
from jeb import jeb
import requests
from datetime import datetime
from flask import render_template

@jeb.route('/')
@jeb.route('/index')
def index():
    return "long live jeb" + "<br><br>" + check_ips()

def get_ip(addr):
    resp = requests.get(addr)
    if resp.ok:
        return resp.text
    else:
        return "Failure: " + resp.reason

@jeb.route('/ip')
def check_ips():
    jebcam = get_ip("https://icanhazip.com")
    deluge = get_ip("http://192.168.0.9:8118")
    dt = datetime.now()
    template = '''
    My IP:  {}<br>
    Torrent Ip:  {}<br>
    Page served:  {}<br>
    '''
    return template.format(jebcam, deluge, dt)

@jeb.route('/status')
def get_status():
    status = {'playing': False}
    return render_template('status.html', date=datetime.now(), ip='123', status=status)

#class Player:


