
// use KeyboardEvent.key instead of .code to permit combinations
// (e.g. '<' instead of 'Shift' + 'Comma')
// Tweakable constants are done in python, hence "skip +1" vs "volume_up"
// This should only invoke entries in /srv/api.py
const KEY_MAPPINGS = {
    "0":        "seek_start",
    ArrowLeft:  "seek_back",
    ArrowRight: "seek_forward",
    ArrowUp:    "volume_up",
    ArrowDown:  "volume_down",
    "m":        "mute",
    "M":        "unmute",
    "s":        "subtitles 1",
    "S":        "subtitles 0",
    "<":        "skip -1",
    ">":        "skip +1",
    " ":        "pause",
};

document.onkeydown = function(e) {
    // skip browser actions
    if (e.altKey != false) { return; }
    // skip text entry
    if (document.activeElement.id != "body") { return; }

    let text = KEY_MAPPINGS[e.key];
    if (text != undefined) {
        document.getElementById("command").value = text;
        send_cmd(text);
    }
}

// play selection in "content" box
function play_selection() {
    const selection = document.getElementById("selection").value;
    dispatch_request("api/select", { selection });
}

// make a request, paying no attention to its success (params are optional)
// NOTE this function is duplicated because ajax is dumb
function dispatch_request(rel_url, params) {
    let data = new FormData();
    for (let k in params) { data.append(k, params[k]); }
    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", rel_url, true);
    xhttp.send();
}

document.getElementById("selection").addEventListener("keydown", function(e) {
    if (e.key === "Enter") { play_selection(); }
}, false);

