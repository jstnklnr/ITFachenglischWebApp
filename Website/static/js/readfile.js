document.addEventListener("DOMContentLoaded", function(event){

var doc = document.querySelectorAll(".square-border");
number = doc.length;



var square = document.getElementsByClassName("square-border");
var font = document.getElementsByClassName("selection_text");

switch (number) {
    case 1:
        setStyle(square, "15%", "15%");     
      break;
    case 2:
        setStyle(square, "15%", "15%");    
      break;
    case 3:
        setStyle(square, "15%", "15%");     
        break;
    case 4:
        setStyle(square, "15%", "15%");     
        break;
    case 5:
        setStyle(square, "13%", "13%");
        break;
    case 6:
        setStyle(square, "10%", "10%"); 
        break;
    case 7:
        setStyle(square, "10%", "10%");
        break;
    case 8:
        setStyle(square, "8%", "8%");     
        break;
    case 9:
        setStyle(square, "10%", "10%");     
        break;    
    case 10:
        setStyle(square, "10%", "10%"); 
          break;
    case 11:
        setStyle(square, "10%", "10%");
          break;
    case 12:
        setStyle(square, "10%", "10%");     
          break;
    case 13:
        setStyle(square, "10%", "10%");     
          break;  
    case 14:
        setStyle(square, "5%", "5%");     
          break; 
    default:
      // Anweisungen werden ausgeführt,
      // falls keine der case-Klauseln mit expression übereinstimmt
      break;
  }

  function setStyle ( square,  width,  paddingBottom)
  {
    for (let index = 0; index < square.length; index++) {
        square[index].style.width = width;
        square[index].style.paddingBottom = paddingBottom;

    }

  }
  
  function setFont (font, fontsize)
  {
    for (let y = 0; y < font.length; y++) {
        font[y].style.fontSize = fontsize; 
    }

  }




/*
var div = document.createElement("div");
div.style.width = "100px";
div.style.height = "100px";
div.style.background = "red";
div.style.color = "white";
div.innerHTML = "Hello";

document.getElementById("main").appendChild(div);
*/
  });