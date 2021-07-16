document.addEventListener("DOMContentLoaded", function(event){


var number = document.querySelectorAll('square-border').length;
Add(number);
    
    
    function Add(number)
    {   
        for (let index = 0; index < number; index++) 
        {
            var square = document.createElement("div");
            square.className = "square-border";

            var text = document.createElement("div");
            text.className = "square-text";
            text.innerHTML= "Hello";

            if (number <= 6)
            {
                document.getElementById("main").appendChild(square)
                square.appendChild(text);
            }
            else
            {
                if (index < number/2)
                    {
                        document.getElementById("main").appendChild(square)
                        square.appendChild(text);
                    }
                else
                    {
                        document.getElementById("main2").appendChild(square)
                        square.appendChild(text);
                    }
            }
        }   
    }
    

var style_square = document.getElementsByClassName("square-border");
var font_square = document.getElementsByClassName("square-text")

    switch (number) {
        case 1:
            setStyle(style_square, "15%", "15%", font, "10px");     
          break;
        case 2:
            setStyle(style_square, "15%", "15%");    
          break;
        case 3:
            setStyle(style_square, "13%", "13%");     
            break;
        case 4:
            setStyle(style_square, "14%", "14%");     
            break;
        case 5:
            setStyle(style_square, "12%", "12%");
            break;
        case 6:
            setStyle(style_square, "10%", "10%"); 
            break;
        case 7:
            setStyle(style_square, "10%", "10%");
            break;
        case 8:
            setStyle(style_square, "10%", "10%");     
            break;
        case 9:
            setStyle(style_square, "10%", "10%");     
            break;    
        case 10:
            setStyle(style_square, "10%", "10%"); 
              break;
        case 11:
            setStyle(style_square, "9%", "9%");
              break;
        case 12:
            setStyle(style_square, "9%", "9%");     
              break;
        case 13:
            setStyle(style_square, "8%", "8%");     
              break;  
        case 14:
            setStyle(style_square, "8%", "8%");     
              break; 
        default:
          // Anweisungen werden ausgeführt,
          // falls keine der case-Klauseln mit expression übereinstimmt
          break;
      }
    
      function setStyle ( style_square,  width,  paddingBottom)
      {
        for (let index = 0; index < style_square.length; index++) 
        {
            style_square[index].style.width = width;
            style_square[index].style.paddingBottom = paddingBottom;
        }
      }

});