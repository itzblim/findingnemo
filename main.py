import uri_finder as Finder
import google_ocr as Ocr
import highlight as Highlight
import dl_stge as Dl_stge


def process_images(img_uri_list):
    """
    Downloads a list of images and recognises the text in the image.
    Returns the processed data as a tuple.
    """
    img_id_list = Dl_stge.store_images(img_uri_list)
    text_map_list = list()
    for img_uri in img_uri_list:
        text_map_list.append(Ocr.get_text_map(img_uri))
    return (img_id_list, text_map_list, img_uri_list)


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
    images_matched = list()
    for i in range(len(img_data[0])):
        no_of_image_matches = Highlight.highlight_matches(
            Dl_stge.get_original(img_data[0][i]),
            img_data[1][i],
            query,
            Dl_stge.get_new(img_data[0][i]))
        for j in range(no_of_image_matches):
            images_matched.append(i)
    return images_matched

def process_website_data(url):
    """
    Takes in the URL for a website.
    Processes the images and returns the image data.
    """
    return process_images(Finder.get_image_urls(url))


def load_url(url):
    cached_data = Dl_stge.retrieve_website_data(url)
    if (cached_data == -1):
        website_data = process_website_data(url)
        Dl_stge.store_website_data(website_data, url)
        return website_data
    Dl_stge.store_images(cached_data[2])
    return cached_data


# Input website
# input_url = "https://www.channelnewsasia.com/news/world/websites-down-reddit-amazon-widespread-internet-outage-14971992"

# # Preprocess the website's images
# cna = load_url(input_url)

# # Run a query on the website's images
# find(cna, "mer info")

# # For debugging
# print_text(cna)

# Backend

# dynamically loaded webpages? <--?
#
# possible creation of requirements.txt at the end -- Bryan

# Replace images in source code -- Bryan
# Link images so that we can jump to the matched images in the site.

# Frontend
# look up chrome extension videos <------- !!
