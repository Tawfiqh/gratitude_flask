"use strict";
function urlParamsGetPassword() {
    var urlParams = new URLSearchParams(window.location.search);
    var password = urlParams.get('password');
    return password;
}
// Default simple url - no password
var gratitudeURL = "/gratitude_simple";
// If a password is found, then set new URL endpoint.
var myPassword = urlParamsGetPassword();
if (myPassword) {
    gratitudeURL = "/gratitude?password=" + myPassword;
}
function getNewGratitudeReason() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var textDisplay = document.getElementById("gratitude");
            textDisplay.innerHTML = this.responseText;
        }
    };
    console.log("Firing off new request to:" + gratitudeURL);
    xhr.open("GET", gratitudeURL);
    xhr.send();
}
getNewGratitudeReason();
document.body.addEventListener('click', getNewGratitudeReason, true);
