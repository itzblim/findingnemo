console.log("Check if content.js is running");

function replaceImages() {
    let images = document.querySelectorAll('img');

    for (var i = 0; i < imgArray.length; i++) {
        for (elt of images) {
            if (elt.src == imgArray[i]) {
                let file = 'images/cat.jpg';
                let url = chrome.extension.getURL(file);
                elt.src = url;
            }
        }
    }
}

//To find a slightly more permanent fix than this. 
//Somehow functions which wait for webpage to load doesnt fully wait for it to load

//this function must load only after url finder has finish loading 
setTimeout(() => { replaceImages(); }, 10000)



