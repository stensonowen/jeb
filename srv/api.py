
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

