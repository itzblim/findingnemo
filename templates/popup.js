var textHits = 0
var imgHits = 0
var totalHits = textHits + imgHits
var counterPosition = 1
var testImgArray = [1, 2, 3, 4, 5]



document.getElementById("searchBar").addEventListener("keypress", searchBar)
document.getElementById("hitCounter").innerHTML = hitCounter()
document.getElementById("arrowUp").addEventListener("click", upArrow)
document.getElementById("arrowDown").addEventListener("click", downArrow)
document.getElementById("escape").addEventListener("click", escape)
document.getElementById("runButton").addEventListener("click", showRunAlert)
document.getElementById("textHits").innerHTML = textHits
document.getElementById("imgHits").innerHTML = imgHits

function searchBar(event) {
    searchElem = document.getElementById("searchBar").value
    chrome.tabs.query({ 'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT },
        function (tabs) {
            currentUrl = (tabs[0].url)
        }
    );
    if (event.key === "Enter") {
        // alert("You are searching: " + searchElem) //forchecking
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: "http://localhost:5000/search-link/",
            traditional: "true",
            data: JSON.stringify({ searchElem }),
            dataType: "json"
        })

        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: "http://localhost:5000/currentUrl-link/",
            traditional: "true",
            data: JSON.stringify({ currentUrl }),
            dataType: "json"
        })

    }
    return false
}

function hitCounter() {
    if (totalHits == 0) {
        return `0/0`
    } else {
        return `${counterPosition}/${totalHits}`
    }
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



