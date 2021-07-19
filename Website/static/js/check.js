function check(){
    const xhttp = new XMLHttpRequest();
    fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({"translation": document.getElementById("input__field").value})    
    }).then(res => {
        if(res.redirected){
            console.log(res.r)
            document.getElementById("continue").addEventListener("click", ()=>{
                window.location.replace(res.url);
            })
        }
      });
}