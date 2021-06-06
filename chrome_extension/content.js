console.log("Check if content.js is running");

// this doesnt work. Need to find a way to read in txt file output into this javascript file 
// fetch("file:///C:/Users/bubuw/findingnemo/chrome_extension/img_urls.txt")
//     .then(response => response.text())
//     .then(text => console.log(text))
// outputs the content of the text file


let images = document.querySelectorAll('img');

for (elt of images) {
    if (elt.src == "https://www.channelnewsasia.com/image/13479566/0x0/1920/1764/985083649d9865bbaa1fb2efeda0caa6/aJ/infographic--how-the-psle-score-is-determined.png") {
        let file = 'images/cat.jpg';
        let url = chrome.extension.getURL(file);
        elt.src = url;
    }

}

