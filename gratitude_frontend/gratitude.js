const urlParams = new URLSearchParams(window.location.search);
const myPassword = urlParams.get('password');
if (myPassword != null) {
    gratitudeURL = "/gratitude?password=" + myPassword
}
else {
    gratitudeURL = "/gratitude_simple"
}

xhr = new XMLHttpRequest();

xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("gratitude").innerHTML = this.responseText;
    }
};
xhr.open("GET", gratitudeURL);

xhr.send();