
document.onkeydown = checkKey;

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
        console.log("UP");
    }
    else if (e.keyCode == '40') {
        // down arrow
        console.log("down");
    }
    else if (e.keyCode == '37') {
       // left arrow
        console.log("le");
    }
    else if (e.keyCode == '39') {
       // right arrow
        console.log("r");
    }
}

function get_status() {
    console.log("status");
}

function cmd_volume_up()    { console.log("volume up"); }
function cmd_volume_down()  { console.log("volume up"); }
function cmd_skip_back()    { console.log("back 10 seconds"); }
function cmd_skip_forward() { console.log("forward 10 seconds"); }

