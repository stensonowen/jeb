
document.onkeydown = checkKey;

const CMD_MAPPINGS = {
    ArrowLeft:      cmd_skip_back,
    ArrowRight:     cmd_skip_forward,
    ArrowUp:        cmd_volume_up,
    ArrowDown:      cmd_volume_down,
};

function checkKey(e) {

    e = e || window.event;

    // ignore modifiers (which are probably intended for the browser)
    if (e.getModifierState() === true) {
        return;
    }

    //console.log(e);

    let func = CMD_MAPPINGS[e.code];
    if (func != undefined) {
        func();
    }

}

