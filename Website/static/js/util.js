window.addEventListener("load", () => {
    document.getElementById("checkButton").addEventListener("click", check);
});

function check() {
    fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"translation": document.getElementById("controlTextarea1").value})
    }).then(res => {
            res.json().then(data => {
                console.log(data.Success)
                if(!data.Success){
                    checkMessage =  `<div id="alert" class="alert alert-danger" role="alert"></div>`
                    document.getElementById("headline").innerHTML = checkMessage
                    document.getElementById("alert").innerHTML = "Wrong translation. Possible translation: " + data.Translations.join(', ');
                }
                else if(data.Success){
                    checkMessage = `<div id="alert" class="alert alert-success" role="alert"></div>`
                    document.getElementById("headline").innerHTML = checkMessage;
                    document.getElementById("alert").innerHTML = "Right.";
                }

                let checkButton = document.getElementById("checkButton");
                checkButton.setAttribute("href", "vocabulary");
                checkButton.removeEventListener("click", check);
                checkButton.getElementsByTagName("h4")[0].innerText = "Continue";
            });
        });
        
}