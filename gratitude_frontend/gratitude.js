"use strict";
var urlParams = new URLSearchParams(window.location.search);
var myPassword = urlParams.get('password');
var gratitudeURL;
if (myPassword != null) {
    gratitudeURL = "/gratitude?password=" + myPassword;
}
else {
    gratitudeURL = "/gratitude_simple";
}
var xhr = new XMLHttpRequest();
var document = document || { getElementById: "" };
xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        var textDisplay = document.getElementById("gratitude");
        textDisplay.innerHTML = this.responseText;
    }
};
xhr.open("GET", gratitudeURL);
xhr.send();
