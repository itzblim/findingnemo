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
        Highlight.highlight_matches(Dl_stge.get_original(
            img_data[0][i]), img_data[1][i], query, Dl_stge.get_new(img_data[0][i]))


def get_website_data(url):
    """
    Takes in the URL for a website.
    Processes the images and returns the image data.
    """
    return process_images(Finder.get_image_urls(url))


# Input website
input_url = "https://www.channelnewsasia.com/news/singapore/moe-psle-new-scoring-system-secondary-1-cut-off-point-13479238"

# Preprocess the website's images
nlb = get_website_data(input_url)

# Run a query on the website's images
find(nlb, "psle")

# For debugging
print_text(nlb)


#
# Join the disjoint characters
# .svg see if can convert
# some nested images dun come up
#
