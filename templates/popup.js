var textHits = 20
var imgHits = 100
var totalHits = textHits + imgHits
var counterPosition = 1
var testImgArray = [1, 2, 3, 4, 5]


document.getElementById("hitCounter").innerHTML = hitCounter()
document.getElementById("arrowUp").addEventListener("click", upArrow)
document.getElementById("arrowDown").addEventListener("click", downArrow)
document.getElementById("escape").addEventListener("click", escape)
document.getElementById("runButton").addEventListener("click", showRunAlert)
document.getElementById("textHits").innerHTML = textHits
document.getElementById("imgHits").innerHTML = imgHits

function hitCounter() {
    return `${counterPosition}/${totalHits}`
}

function counterPositionHelper(direction) {
    if (direction == "up") {
        counterPosition--
    } else {
        counterPosition++
    }
    if (counterPosition < 1) {
        counterPosition = totalHits
    } else if (counterPosition > totalHits) {
        counterPosition = 1
    }
    return counterPosition
}

function upArrow() {
    counterPosition = counterPositionHelper("up")
    document.getElementById("hitCounter").innerHTML = hitCounter()
}

function downArrow() {
    counterPosition = counterPositionHelper("down")
    document.getElementById("hitCounter").innerHTML = hitCounter()
}

function escape() {
    window.close()
}

function showRunAlert() {
    var myText = "Proof of Concept";
    alert(myText);
}



