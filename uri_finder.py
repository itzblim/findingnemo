from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import requests
import sys
from yarl import URL
import validators
import os
import json

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
#     url refers to the url of the individual img,
#     website_url refers to the url of the entire webpage

def abs_relative(url, website_url):
    if is_absolute(url):
        if url.startswith("http://"):
            return url[:4] + "s" + url[4:]
        elif url.startswith("https://"):
            return url
        elif url.startswith("//"):
            return "https:" + url
        else:
            return "https://" + url
    else:
        return "https://" + URL(website_url).host + url


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
            if img_url.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                temp_list2.append(img_url)

    # Prefix the src/data-src urls with the appropriate url_prefixes
    for img_url in temp_list2:
        temp_list3.append(abs_relative(img_url, website_url))

    # Remove image_urls if they are not valid
    for img_url in temp_list3:
        if is_invalid(img_url):
            print("Removed: " + img_url)
        else:
            image_urls.append(img_url)

    return image_urls


def generate_imgUrlJS(website_url):
    return json.dumps(get_image_urls(website_url))

