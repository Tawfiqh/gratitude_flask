function urlParamsGetPassword() : string | null{
    const urlParams = new URLSearchParams(window.location.search);
    const password :string | null = urlParams.get('password');

    return password
}


// Default simple url - no password
var gratitudeURL : string =  "/gratitude_simple";

// If a password is found, then set new URL endpoint.
const myPassword : string | null = urlParamsGetPassword();
if ( myPassword ) {
    gratitudeURL = "/gratitude?password=" + myPassword
}


function getNewGratitudeReason(){
    
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var textDisplay : HTMLElement = document.getElementById("gratitude") as HTMLElement
            textDisplay.innerHTML = this.responseText;
        }
    };

    console.log("Firing off new request to:" + gratitudeURL)
    xhr.open("GET", gratitudeURL);

    xhr.send();
}

getNewGratitudeReason()

document.body.addEventListener('click', getNewGratitudeReason, true); 
