# step1: Get the urls of all images on the website--done
# step1a: Verify all the urls are valid--done
# step2: filter out those images with words-- not done

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import requests
from yarl import URL

# "http://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"


# Variables
input_url = "https://eresources.nlb.gov.sg/Main/"
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


def url_prefix(url):
    """
    Prefixes the URL with http://...
    """
    return URL(url).scheme + "://" + URL(url).host


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

    # Remove src/data-src info which has None, "", or doesn't start with "/"
    for img_url in temp_list1:
        if img_url != None and img_url != "":
            if img_url[0] == "/":
                temp_list2.append(img_url)

    # Prefix the src/data-src urls with the appropriate url_prefixes
    for img_url in temp_list2:
        image_urls.append(url_prefix(input_url) + img_url)

    # Remove image_urls if they are not valid
    for img_url in image_urls:
        if not is_valid(img_url):
            print("Removed: " + img_url)
            image_urls.remove(img_url)

    return image_urls


print(get_image_urls(input_url))
