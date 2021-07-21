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
                checkMessage = data.Success ? `<div id="alert" class="alert alert-success" role="alert"></div>` : `<div id="alert" class="alert alert-danger" role="alert"></div>`;
                document.getElementById("headline").innerHTML = checkMessage
                message = "";

                if(data.Translations)
                    message = (data.Success ? "Correct." : "Wrong.") + " Possible translation: " + data.Translations.join(", ");
                else if(data.Phrase)
                    message = (data.Success ? "Correct." : "Wrong.") + " Answer: " + data.Phrase;

                document.getElementById("alert").innerHTML = message;

                let checkButton = document.getElementById("checkButton");
                checkButton.setAttribute("href", checkHref);
                checkButton.removeEventListener("click", check);
                checkButton.getElementsByClassName("btn")[0].innerText = "Continue";
            });
        });
        
}