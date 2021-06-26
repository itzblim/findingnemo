console.log("Check if content.js is running");
var localImgArray = ['images/cat.jpg', 'images/cat2.jpg', 'images/cat3.jpg']

function replaceImages() {
    let images = document.querySelectorAll('img');

    for (var i = 0; i < imgArray.length; i++) {
        for (elt of images) {
            if (elt.src == imgArray[i]) {
                let file = localImgArray[i];
                let url = chrome.extension.getURL(file);
                elt.src = url;
                elt.setAttribute("id", `Pic${i}`)
            }
        }
    }
}


//To find a slightly more permanent fix than this. 
//Somehow functions which wait for webpage to load doesnt fully wait for it to load

//this function must load only after url finder has finish loading 
setTimeout(() => { replaceImages(); }, 5000)



