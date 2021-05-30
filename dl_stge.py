import requests
import os
import shutil


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
