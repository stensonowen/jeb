#!/usr/bin/env python3

import conn
from conn import get_cached_db as db
from change import Change

# defaults
Vup = Change.rel(+1)
Vdn = Change.rel(-1)
Sfw = Change.rel(+10)
Sbk = Change.rel(-10)

# this should handle all entries in /site/control.js
COMMANDS = {
        "seek_back":    lambda x="-9": db().seek(x),  # seconds
        "seek_forward": lambda x="+9": db().seek(x),
        "seek_start":   lambda _     : db().seek(),
        "seek":         lambda x="0" : db().seek(x),
        "volume_up":    lambda x="+1": db().volume(x),# TODO unit? dB?
        "volume_down":  lambda x="-1": db().volume(x),
        "mute":         lambda _     : db().mute(),   # toggle
        "unmute":       lambda _     : db().mute(False),
        "skip_previous":lambda x="-1": db().skip(-1),
        "skip_next":    lambda x="+1": db().skip(+1),
        "pause":        lambda _     : db().pause(),
        #"quit":         TODO,
        #"chapter next|[rev": TODO,
        #"fwd_text":     TODO,
        # "seek_back:"  lambda(r=-10): seek(r),
        }

