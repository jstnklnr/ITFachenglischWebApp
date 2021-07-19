document.getElementById("check").onclick(() => {
    const xhttp = new XMLHttpRequest();
    fetch("/check", {
        method: "POST",
        body: {"translation": document.getElementById("input_field").value}
    }).then(res => {
        console.log(res)
      });
})