var refreshes = 0;

function replaceImages(oldLinks, newLinks) {
    console.log("Replacing images...")
    let images = document.querySelectorAll('img');
    var suffix = ""
    if (refreshes != 0) {
        suffix = "?t=" + refreshes
    }
    refreshes++
    for (var i = 0; i < oldLinks.length; i++) {
        for (elt of images) {
            if (elt.src == oldLinks[i] + suffix) {
                let file = newLinks[i];
                let url = file + "?t=" + refreshes
                elt.src = url;
                elt.srcset = url;
                elt.setAttribute("id", `Pic${i}`)
                console.log("Image replaced.")
            }
        }
    }
    console.log("All image replacements completed.")
}

chrome.runtime.onMessage.addListener((msg, sender, response) => {
    if ((msg.from === 'popup') && (msg.subject === 'imglists')) {
      replaceImages(msg.oldImgs, msg.newImgs)
      response("Successful!");
    }
  });




