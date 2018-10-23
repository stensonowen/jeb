
# apt install python3-dbus
import dbus
from typing import Optional

'''
def get_dbus_pid() -> Optional[int]:
    try:
        with open("/tmp/omxplayerdbus.pi.pid") as f:
            s = f.read().strip()
            return int(s)
    except Exception as e:
        print("Failed to get pid: {}".format(e))
        # return None
        raise e
        '''

# may throw file not found
def get_dbus_addr() -> str:
    # for more logic see bus_finder.py:find_address_file
    # from https://github.com/willprice/python-omxplayer-wrapper (LGPL)
    return open("/tmp/omxplayerdbus.pi").read().strip()

'''
def loop_get_dbus_addr() -> str:
    while True:
        try:
            with open("/tmp/omxplayerdbus.pi") as f:
                s = f.read().split()
                if ':' in s:
                    return s
                else:
                    raise Exception("Invalid omx pidfile")
        except Exception as e:
            print("Failed to get omx pidfile")
            time.sleep(0.1)
            '''


def init_dbus(addr):
    omx_str = "org.mpris.MediaPlayer2" # note no trailing '.'
    dbus_name = omx_str + ".omxplayer"
    bus = dbus.bus.BusConnection(addr)
    proxy = bus.get_object(dbus_name, omx_str, introspect=False)
    intf_root = dbus.Interface(proxy, omx_str)
    intf_play = dbus.Interface(proxy, omx_str + ".Player")
    intf_prop = dbus.Interface(proxy, omx_str + ".Properties")

# cached dbus connection
class DbusConn:
    def __init__(self):
        self.bus: dbus.bus.BusConnection = None
        self.proxy = None
        self.root_iface: dbus.Interface = None
        self.play_iface: dbus.Interface = None
        self.prop_iface: dbus.Interface = None
        self.addr: str = None

    # may throw file not found
    def _get_dbus_addr() -> str:
        # for more logic see bus_finder.py:find_address_file
        # from https://github.com/willprice/python-omxplayer-wrapper (LGPL)
        return open("/tmp/omxplayerdbus.pi").read().strip()

    def refresh(self):
        self.addr = DbusConn._get_dbus_addr()
        omx_str = "org.mpris.MediaPlayer2" # note no trailing '.'
        dbus_name = omx_str + ".omxplayer"
        self.bus = dbus.bus.BusConnection(self.addr)
        self.proxy = self.bus.get_object(dbus_name, omx_str, introspect=False)
        self.root_iface = dbus.Interface(self.proxy, omx_str)
        self.play_iface = dbus.Interface(self.proxy, omx_str + ".Player")
        self.prop_iface = dbus.Interface(self.proxy, omx_str + ".Properties")

    def cache_valid(self) -> bool:
        # TODO I don't think this will work
        return self.addr == _get_dbus_addr()

    # ACTIONS
    def pause():
        # TODO toggle
        self.play_iface.Pause()
        # unpause: self.play_iface.Play()



COMMANDS = {
        "seek_back":    lambda: seek(-10),  # seconds
        "seek_forward": lambda: seek(+10),
        "seek_start":   lambda: seek(),
        "volume_up":    lambda: volume(+3), # dB
        "volume_down":  lambda: volume(-3),
        "mute":         lambda: volume(),
        "skip_previous":lambda: skip(-1),
        "skip_next":    lambda: skip(+1),
        "pause":        lambda: pause(),
        # "seek_back:"  lambda(r=-10): seek(r),
        }

def volume(rel=None):
    if rel:
        print("Pretend I changed the volume relatively by {}".format(rel))
    else:
        print("Pretend I toggled mute")

def seek(rel=None):
    if rel:
        print("Pretend I seeked relatively by {}".format(rel))
    else:
        print("Pretend I sought to the beginning")

def skip(direction):
    print("Pretend I skipped {}".format(direction))

def pause():
    # maybe add absolute vs toggle option?
    print("Pretend I toggled pause")

