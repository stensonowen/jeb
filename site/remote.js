
export function foo() {
    console.log("cal fo");
}

console.log("I'm here it me remote");

function loadDoc() {
    console.log("loaded doc");
}

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

export function send_cmd(data) {
    console.log("caled send cmid");
}

// hello.mjs
export function hello2(text) {
    const div = document.createElement('div');
    div.textContent = `Hello ${text}`;
    document.body.appendChild(div);
    console.log("hello'd");
}
