
console.log("ran api.js");

function get_status() {
    console.log("status");
}

function cmd_volume_up()    { console.log("volume up"); }
function cmd_volume_down()  { console.log("volume up"); }
function cmd_skip_back()    { console.log("back 10 seconds"); }
function cmd_skip_forward() { console.log("forward 10 seconds"); }
function cmd_skip_prev()    { console.log("prev"); }
function cmd_skip_next()    { console.log("next"); }

function loadDoc() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        document.getElementById("demo").innerHTML = "foo";
        console.log(this);
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            document.getElementById("demo").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "getmedaddy", true);
    xhttp.send();
}
