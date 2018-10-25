
# apt install python3-dbus
import dbus
from typing import Optional

DBUS = None

def get_dbus():
    global DBUS
    if DBUS is None:
        DBUS = DbusConn()
        DBUS.refresh()
    elif DBUS.cache_valid() is False:
        DBUS.refresh()
    return DBUS

# cached dbus connection
class DbusConn:
    def __init__(self):
        self.bus = None
        self.proxy = None
        self.root_iface = None
        self.play_iface = None
        self.prop_iface = None
        self.addr = None

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
        self.proxy = self.bus.get_object(dbus_name, "/org/mpris/MediaPlayer2", introspect=False)
        self.root_iface = dbus.Interface(self.proxy, omx_str)
        self.play_iface = dbus.Interface(self.proxy, omx_str + ".Player")
        self.prop_iface = dbus.Interface(self.proxy, "org.freedesktop.DBus.Properties")

    def cache_valid(self) -> bool:
        # TODO I don't think this will work
        return self.addr == _get_dbus_addr()

    # HELPERS
    def _get_property(self, query):
        return self.prop_iface.Get(self.play_iface.dbus_interface, query)

    def _get_pos_ns(self) -> int:
        return self._get_property("Position")

    #def _get_state(self) -> str:
    #    # Playing | Paused
    #    return self._get_property("PlaybackStatus")

    # ACTIONS
    #def pause(self):
    #    self.play_iface.Pause()

    #def unpause(self):
    #    self.play_iface.Play()

    #def can_pause(self) -> bool:
    #    return bool(self._get_property("CanPause"))

    def toggle_pause(self):
        if self._get_property("PlaybackStatus") == "Playing":   # alt 'Paused'
            self.play_iface.Pause()
        else:
            self.play_iface.Play()

    def seek(self, rel=None):
        if rel == 0:
            self.set_pos(0)
        elif self._get_property("CanSeek"):
            self.play_iface.Seek(Int64(rel * 1000.0 * 1000.0))
        else:
            print("Cannot seek")

    def set_pos(self, pos):
        timestamp = Int64(pos * 1000.0 * 1000.0)
        self.play_iface.SetPosition(ObjectPath("/not/used"), timestamp)

    def skip(self, direction):
        if direction == +1:
            self.play_iface.Next()
        elif direction == -1:
            self.play_iface.Previous()
        else:
            print("TODO skip by more than 1 ({}".format(direction))

    def volume(vol=None):
        if vol == 0:
            #if self._player_interface_property('Volume')
            self.play_iface.Mute()
            self.play_iface.Unmute()
        else:
            target = dbus.Double(10**(vol / 2000.0))
            self._player_interface_property('Volume', target)


COMMANDS = {
        "seek_back":    lambda: get_dbus().seek(-10),  # seconds
        "seek_forward": lambda: get_dbus().seek(+10),
        "seek_start":   lambda: get_dbus().seek(),
        "volume_up":    lambda: get_dbus().volume(+3), # dB
        "volume_down":  lambda: get_dbus().volume(-3),
        "mute":         lambda: get_dbus().volume(),
        "skip_previous":lambda: get_dbus().skip(-1),
        "skip_next":    lambda: get_dbus().skip(+1),
        "pause":        lambda: get_dbus().pause(),
        # "seek_back:"  lambda(r=-10): seek(r),
        }

'''
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
'''
