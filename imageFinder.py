# step1: Get the urls of all images on the website--done
# step1a: Verify all the urls are valid--done
# step2: filter out those images with words-- not done

from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import requests
from yarl import URL


# Variables
input_url = "https://eresources.nlb.gov.sg/Main/"
#input_url = "http://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"
image_urls = []
###############


def is_valid(url):
    """
    Checks if url is valid
    """
    try:
        response = requests.get(url)
        return True
    except requests.ConnectionError as exception:
        return False


def is_absolute(url):
    return bool(urlparse(url).netloc)


def url_prefix(url):
    """
    Prefixes the URL with http://...
    """
    return "http://" + URL(url).host


def abs_relative(url):
    if is_absolute(url):
        if url.startswith("http://") or url.startswith("https://"):
            return url
        elif url.startswith("//"):
            return "http:" + url
        # idk if absolute urls only have http and //, so added final check just in case
        else:
            return "http://" + url
    else:
        return url_prefix(input_url) + url


def get_image_urls(website_url):
    """
    Takes in the webpage url
    Returns a list of urls for images on the webpage
    """

    # Variables
    temp_list1 = []
    temp_list2 = []

    # Masks the url to prevent website from rejecting bot and showing HttpError404
    req = Request(website_url,
                  headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    soup = bs(webpage, "html.parser")

    # Filter out info under the "src" or "data-src" tags from imgs
    for img in soup.findAll('img'):
        temp_list1.append(img.get('src'))
        if img.get('src') == None:
            temp_list1.append(img.get('data-src'))

    # Remove src/data-src info which has None, ""
    for img_url in temp_list1:
        if img_url != None and img_url != "":
            if img_url.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', ".svg")):
                temp_list2.append(img_url)

    # Prefix the src/data-src urls with the appropriate url_prefixes
    for img_url in temp_list2:
        image_urls.append(abs_relative(img_url))

    # Remove image_urls if they are not valid
    for img_url in image_urls:
        if not is_valid(img_url):
            print("Removed: " + img_url)
            image_urls.remove(img_url)

    return image_urls


print(get_image_urls(input_url))
