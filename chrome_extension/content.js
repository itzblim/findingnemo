console.log("Check if content.js is running");

function replaceImages() {
    let images = document.querySelectorAll('img');

    for (var i = 0; i < img_array.length; i++) {
        for (elt of images) {
            if (elt.src == img_array[i]) {
                let file = 'images/cat.jpg';
                let url = chrome.extension.getURL(file);
                elt.src = url;
            }
        }
    }
}

//To find a slightly more permanent fix than this. 
//Somehow functions which wait for webpage to load doesnt fully wait for it to load
setTimeout(() => { replaceImages(); }, 5000)



