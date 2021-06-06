from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import requests
import sys
from yarl import URL
import validators
import os.path


# Testing urls
#input_url = "https://eresources.nlb.gov.sg/Main/"
input_url = "http://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"
#input_url = "http://darwin-online.org.uk/content/frameset?viewtype=text&itemID=F1497&pageseq=5"
###############


def is_invalid(url):
    """
    Checks if url is invalid
    """
    return not validators.url(url)


def is_absolute(url):
    return bool(urlparse(url).netloc)


# def url_prefix(url):
#     """
#     Prefixes the URL with https:// or http://
#     """
#     if URL(url).scheme == 'https':
#         return "https://"
#     else:
#         return "http://"


def abs_relative(url):
    if is_absolute(url):
        if url.startswith("http://"):
            return url[:4] + "s" + url[4:]
        elif url.startswith("https://"):
            return url
        elif url.startswith("//"):
            return "https:" + url
        # idk if absolute urls only have http and //, so added final check just in case
        else:
            return "https://" + url
    else:
        return "https://" + URL(input_url).host + url


def get_image_urls(website_url):
    """
    Takes in the webpage url
    Returns a list of urls for images on the webpage
    """

    # Variables
    temp_list1 = []
    temp_list2 = []
    temp_list3 = []
    image_urls = []

    # Masks the url to prevent website from rejecting bot and showing HttpError404
    req = Request(website_url,
                  headers={'User-Agent': 'Mozilla/5.0'})

    webpage = urlopen(req).read()
    soup = bs(webpage, "lxml")

    # Filter out info under the "src" or "data-src" tags from imgs
    for img in soup.find_all('img'):
        temp_list1.append(img.get('src'))
        if img.get('src') == None:
            temp_list1.append(img.get('data-src'))

    # Remove src/data-src info which has None, ""
    for img_url in temp_list1:
        if img_url != None and img_url != "":
            if img_url.endswith(('.svg', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                temp_list2.append(img_url)

    # Prefix the src/data-src urls with the appropriate url_prefixes
    for img_url in temp_list2:
        temp_list3.append(abs_relative(img_url))

    # Remove image_urls if they are not valid
    for img_url in temp_list3:
        if is_invalid(img_url):
            print("Removed: " + img_url)
        else:
            image_urls.append(img_url)

    return image_urls


orig_sys = sys.stdout
save_to_path = 'chrome_extension'
complete_name = os.path.join(save_to_path, "img_urls.txt")
with open(complete_name, 'w') as out:
    sys.stdout = out
    print(len(get_image_urls(input_url)))
    for i in get_image_urls(input_url):
        print(i)
