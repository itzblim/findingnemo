var textHits = 0;
var imgHits = 0;
var totalHits = 0;
var counterPosition = 1;
var newImgArray;
var oldImgArray;
var currentUrl;

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("searchBar").addEventListener("keypress", searchBar);
  document.getElementById("hitCounter").innerHTML = hitCounter();
  document.getElementById("arrowUp").addEventListener("click", upArrow);
  document.getElementById("arrowDown").addEventListener("click", downArrow);
  document.getElementById("escape").addEventListener("click", escape);
  document.getElementById("runButton").addEventListener("click", showRunAlert);
  document.getElementById("textHits").innerHTML = textHits;
  document.getElementById("imgHits").innerHTML = imgHits;
  showRunAlert();
});

function searchBar(event) {
  counterPosition = 1;
  searchElem = document.getElementById("searchBar").value;
  if (event.key === "Enter") {
    $.ajax({
      type: "POST",
      contentType: "application/json;charset=utf-8",
      url: "http://localhost:5000/search-link/",
      traditional: "true",
      data: JSON.stringify({ searchElem }),
      dataType: "json",
      complete: function () {
        $.ajax({
          type: "GET",
          contentType: "application/json;charset=utf-8",
          url: "http://localhost:5000/getImgUrl-link/",
          dataType: "json",
          success: function (res) {
            var n = res.length / 2;
            newImgArray = res
              .slice(0, n - 1)
              .map((x) =>
                "http://localhost:8000/templates/images/new/".concat(x)
              );
            chrome.tabs.query(
              { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
              function (tabs) {
                chrome.tabs.sendMessage(
                  tabs[0].id,
                  {
                    from: "popup",
                    subject: "imglists",
                    oldImgs: newImgArray,
                    newImgs: newImgArray,
                  },
                  function (res) {}
                );
                upArrow();
              }
            );
          },
        });
      },
    });
    //word search done here
    if (searchElem) {
      chrome.tabs.query(
        {
          active: true,
          lastFocusedWindow: true,
        },
        function (tabs) {
          chrome.tabs.executeScript(tabs[0].id, { file: "searchText.js" });
        }
      );
    }
  }
}

function hitCounter() {
  if (totalHits == 0) {
    return `0/0`;
  } else {
    return `${counterPosition + 1}/${totalHits}`;
  }
}

function counterPositionHelper(direction) {
  if (direction == "up") {
    counterPosition--;
  } else {
    counterPosition++;
  }
  if (counterPosition < 0) {
    counterPosition = totalHits - 1;
  } else if (counterPosition > totalHits - 1) {
    counterPosition = 0;
  }
  return counterPosition;
}

function upArrow() {
  changePosition("up");
}

function downArrow() {
  changePosition("down");
}

function changePosition(direction) {
  $.ajax({
    type: "GET",
    contentType: "application/json;charset=utf-8",
    url: "http://localhost:5000/getImgsMatched/",
    dataType: "json",
    success: function (res) {
      imgHits = res.length;
      totalHits = textHits + imgHits;
      counterPosition = counterPositionHelper(direction);
      var new_link = currentUrl + "#Pic" + res[counterPosition];
      chrome.tabs.query(
        { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
        function (tabs) {
          chrome.tabs.update(
            tabs[0].id,
            {
              url: new_link,
            },
            function (res) {}
          );
        }
      );
      document.getElementById("hitCounter").innerHTML = hitCounter();
      document.getElementById("imgHits").innerHTML = imgHits;
    },
  });
}

function escape() {
  window.close();
}

function showRunAlert() {
  chrome.tabs.query(
    { active: true, windowId: chrome.windows.WINDOW_ID_CURRENT },
    function (tabs) {
      currentUrl = tabs[0].url.split("#")[0];
      $.ajax({
        type: "POST",
        contentType: "application/json;charset=utf-8",
        url: "http://localhost:5000/postCurrentUrl-link/",
        traditional: "true",
        data: JSON.stringify({ currentUrl }),
        dataType: "json",
        complete: function (data) {
          $.ajax({
            type: "GET",
            contentType: "application/json;charset=utf-8",
            url: "http://localhost:5000/getImgUrl-link/",
            dataType: "json",
            success: function (res) {
              var n = res.length / 2;
              newImgArray = res
                .slice(0, n - 1)
                .map((x) =>
                  "http://localhost:8000/templates/images/new/".concat(x)
                );
              oldImgArray = res.slice(n, res.length - 1);
              chrome.tabs.sendMessage(
                tabs[0].id,
                {
                  from: "popup",
                  subject: "imglists",
                  oldImgs: oldImgArray,
                  newImgs: newImgArray,
                },
                function (res) {}
              );
            },
          });
        },
      });
    }
  );
}
