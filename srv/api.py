
import dbus
import logging

DBUS = None

def try_reset_dbus():
    # refresh dbus, but maintain correct state on exception
    # if anything goes wrong DBUS should be None
    # cache_vaid() and refresh() can throw
    tmp = DBUS or DbusConn()
    tmp.refresh()
    global DBUS
    DBUS = tmp

def db():
    global DBUS
    # refactor warning: preserve this ordering
    # don't call cache_valid if DBUS is None
    if DBUS is None or DBUS.cache_valid() is False:
        try_reset_dbus()
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
        return self.addr == DbusConn._get_dbus_addr()

    # HELPERS
    def _get_property(self, query):
        return self.prop_iface.Get(self.play_iface.dbus_interface, query)

    def _set_property(self, key, value):
        return self.prop_iface.Set(self.play_iface.dbus_interface, key, value)

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

    def pause(self):    # toggle
        if self._get_property("PlaybackStatus") == "Playing":
            self.play_iface.Pause()
        else:   # 'Paused'
            self.play_iface.Play()

    def seek(self, rel=None):
        if rel is None:
            self.set_pos(0)
        elif self._get_property("CanSeek"):
            target_ns = dbus.Int64(rel * 1000.0 * 1000.0) # relative
            self.play_iface.Seek(target_ns)
        else:
            print("Cannot seek")

    def set_pos(self, pos):
        timestamp = dbus.Int64(pos * 1000.0 * 1000.0)
        self.play_iface.SetPosition(dbus.ObjectPath("/not/used"), timestamp)

    def skip(self, direction):
        if direction == +1:
            self.play_iface.Next()
        elif direction == -1:
            self.play_iface.Previous()
        else:
            print("TODO skip by more than 1 ({}".format(direction))

    # no way to check mute status??
    def mute(self):
        self.play_iface.Mute()
        #self.play_iface.Unmute()

    def volume(self, vol=None):
        cur = dbus.Double(self._get_property("Volume"))
        print("Current volume is {}".format(cur))
        if vol == 0:
            #if self._player_interface_property('Volume')
            self.play_iface.Mute()
            self.play_iface.Unmute()
        else:
            #target = dbus.Double(10**(vol / 2000.0))
            target = dbus.Double(10**(vol / 20.0))
            #self._player_interface_property('Volume', target)
            self._set_property("Volume", target)



COMMANDS = {
        "seek_back":    lambda x="-9": db().seek(x),  # seconds
        "seek_forward": lambda x="+9": db().seek(x),
        "seek_start":   lambda _     : db().seek(),
        "seek":         lambda x="0" : db().seek(x),
        "volume_up":    lambda x="+1": db().volume(x),# TODO unit? dB?
        "volume_down":  lambda x="-1": db().volume(x),
        "mute":         lambda _     : db().mute(),   # toggle
        "skip_previous":lambda x="-1": db().skip(-1),
        "skip_next":    lambda x="+1": db().skip(+1),
        "pause":        lambda _     : db().pause(),
        "quit":         TODO,
        "chapter next|[rev": TODO,
        "fwd_text":     TODO,
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
