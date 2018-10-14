
document.onkeydown = key_down_handler;

const TEXT_MAPPINGS = {
    ArrowLeft:      "Rewind",
    ArrowRight:     "Forward",
    ArrowUp:        "Vol+",
    ArrowDown:      "Vol-",
    "<":            "Prev",
    ">":            "Next",
};

function key_down_handler(e) {
    //e = e || window.event;

    // the 'alt' modifier usually signals the browser (e.g. back/forward)
    if (e.altKey != false) {
        return;
    }

    let text = TEXT_MAPPINGS[e.key];
    let widget = document.getElementById("command");
    if (text != undefined) {
        widget.value = text;
        // SUBMIT
    }


}

