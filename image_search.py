#!/usr/bin/env python
# coding: utf-8

# In[61]:


from urllib.parse import urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from yarl import URL
from PIL import Image
from google.cloud import vision
import requests
import io
import os
import time
import shutil
import urllib
import validators

# API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\itzbl\Documents\GoogleCloudPlatform\orbital-2021-a77c895bfae6.JSON"


# Variables
# input_url = "https://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"
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
    soup1 = bs(webpage, "html.parser")
    soup2 = bs(webpage, "lxml")
    soup3 = bs(webpage, "html5lib")

    # Filter out info under the "src" or "data-src" tags from imgs
    for img in soup1.find_all('img'):
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
        temp_list3.append(abs_relative(img_url))

    # Remove image_urls if they are not valid
    for img_url in temp_list3:
        if is_invalid(img_url):
            print("Removed: " + img_url)
        else:
            image_urls.append(img_url)

    return image_urls

def detect_text_uri(uri):
    """
    Detects text in the file located in Google Cloud Storage or on the Web.
    """
    
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    
    response = client.text_detection(image=image)
    
    for i in range(50):
        if (not response.error.message):
            return response
        response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return response

def get_corners(bounding_box):
    """
    Gets the 4 corners of a bounding box.
    """
    return (bounding_box.vertices[0].x,
            bounding_box.vertices[0].y,
            bounding_box.vertices[2].x,
            bounding_box.vertices[2].y)

def get_text_map(uri):
    """
    Retrieves the letters and their bounding boxes from an image.
    """
    response = detect_text_uri(uri)
    text = list()
    boundaries = list()
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        text.append(symbol.text)
                        boundaries.append(get_corners(symbol.bounding_box))
                    text.append(" ")
                    boundaries.append((0,0,0,0))
    return (text, boundaries)

def highlight_regions(img_src, regions, img_dest):
    """
    Takes a source image, highlights regions and saves the result to the destination.
    """
    img = Image.open(img_src)
    for region in regions:
        if (region != (0,0,0,0)):
            img_crop = img.crop(region)
            overlay = Image.new(img_crop.mode, img_crop.size, color = 	(255,255,0))
            img_crop = Image.blend(img_crop, overlay, 0.4)
            img.paste(img_crop, region)
    if (img_dest != "NA"):
        img.save(img_dest)
    return img

def get_matching_regions(text_map, query):
    """
    Retrieves the regions of an image which match the query.
    """
    query = query.lower()
    full_text = "".join(text_map[0]).lower()
    matches = [False] * len(text_map[0])
    
    for i in range(len(text_map[0])):
        next_start = full_text.find(query, i)
        if (next_start == -1):
            break
        else:
            for j in range(len(query)):
                matches[next_start + j] = True
                
    matching_regions = list()
    for i in range(len(matches)):
        if matches[i]:
            matching_regions.append(text_map[1][i])
    
    return matching_regions

def highlight_matches(img_src, text_map, query, img_dest):
    """
    Highlight matches to a query from a source file and save to destintion file.
    """
    highlight_regions(img_src, get_matching_regions(text_map, query), img_dest)
    
def download_image(uri, destination):
    """
    Download an image to a local destination.
    """
    with open(destination, 'wb') as outfile:
        outfile.write(requests.get(uri).content)
    
def create_empty_directory(destination):
    """
    Creates an empty directory, overriding any existing directories.
    """
    if (os.path.exists(destination)):
        shutil.rmtree(destination)
    os.mkdir(destination)

def get_original(img_id):
    """
    Retrieves the original version of a saved image.
    """
    return "original/" + img_id

def get_new(img_id):
    """
    Retrieves the highlighted version of a saved image.
    """
    return "new/" + img_id

def store_images(img_uri_list):
    """
    Downloads a list of images from their links and returns their IDs.
    """
    create_empty_directory("original")
    create_empty_directory("new")
    img_id_list = list()
    for i in range(len(img_uri_list)):
        image_extension = img_uri_list[i].split(".")[-1]
        image_id = str(i) + "." + image_extension
        download_image(img_uri_list[i], get_original(image_id))
        shutil.copyfile(get_original(image_id), get_new(image_id))
        img_id_list.append(image_id)
    return img_id_list

def process_images(img_uri_list):
    """
    Downloads a list of images and recognises the text in the image.
    Returns the processed data as a tuple.
    """
    img_id_list = store_images(img_uri_list)
    text_map_list = list()
    for img_uri in img_uri_list:
        text_map_list.append(get_text_map(img_uri))
    return (img_id_list, text_map_list)

def print_text(img_data):
    """
    Prints the text from a tuple of processed images.
    """
    for i in range(len(img_data[0])):
        print(img_data[0][i] + ":")
        print("".join(img_data[1][i][0]))
        

def find(img_data, query):
    """
    Takes in the processed data for a set of images and a query.
    Highlights each image's matches and saves them accordingly.
    """
    for i in range(len(img_data[0])):
        highlight_matches(get_original(img_data[0][i]), img_data[1][i], query, get_new(img_data[0][i]))

def get_website_data(url):
    """
    Takes in the URL for a website.
    Processes the images and returns the image data.
    """
    return process_images(get_image_urls(input_url))


# In[65]:


# Input website
input_url = "https://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"


# In[66]:


# Preprocess the website's images
nlb = get_website_data(input_url)


# In[67]:


# Run a query on the website's images
find(nlb, "psle")


# In[68]:


# For debugging
print_text(nlb)


# In[ ]:


#
# Join the disjoint characters
# .svg see if can convert
# some nested images dun come up
# 

