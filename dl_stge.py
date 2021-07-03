import requests
import os
import shutil
import pickle
import hashlib
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


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
    return "templates/images/original/" + img_id


def get_new(img_id):
    """
    Retrieves the highlighted version of a saved image.
    """
    return "templates/images/new/" + img_id


def store_images(img_uri_list):
    """
    Downloads a list of images from their links and returns their IDs.
    """
    create_empty_directory("templates/images/original/")
    create_empty_directory("templates/images/new/")
    img_id_list = list()
    for i in range(len(img_uri_list)):
        image_extension = img_uri_list[i].split(".")[-1]
        image_id = str(i) + "." + image_extension
        download_image(img_uri_list[i], get_original(image_id))
        if (image_extension == "svg"):
            svg_file = svg2rlg(get_original(image_id))
            converted_image_id = str(i) + ".png"
            renderPM.drawToFile(svg_file, get_original(converted_image_id))
            os.remove(get_original(image_id))
            image_id = converted_image_id
        shutil.copyfile(get_original(image_id), get_new(image_id))
        img_id_list.append(image_id)
    return img_id_list

def get_cache_path(url):
    return "cache/" + str(hashlib.sha256(url.encode()).hexdigest()) + '.wdata'

def store_website_data(website_data, url):
    if (not os.path.exists("cache/")):
        os.mkdir("cache/")
    pickle.dump(website_data, open(get_cache_path(url), 'wb'))
    return 1


def retrieve_website_data(url):
    if (not os.path.exists(get_cache_path(url))):
        return -1
    
    return pickle.load(open(get_cache_path(url), 'rb'))
