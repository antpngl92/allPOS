var timeoutInMiliseconds = 60000000; // change to 60 000
var timeoutId; 
  
function startTimer() { 
    timeoutId = window.setTimeout(doInactive, timeoutInMiliseconds)
}
  
function doInactive() {
    location.replace("/logout/")
}
 
function setupTimers () {
    document.addEventListener("mousemove", resetTimer, false);
    document.addEventListener("mousedown", resetTimer, false);
    document.addEventListener("keypress", resetTimer, false);
    document.addEventListener("touchmove", resetTimer, false);
     
    startTimer();
}
 
$(document).ready(function(){
    setupTimers();
})
function resetTimer() { 
    window.clearTimeout(timeoutId)
    startTimer();
}