from google.cloud import vision
import os
import api_key as api_key


# API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"{}".format(api_key.key_str)


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
                    boundaries.append((0, 0, 0, 0))
    return (text, boundaries)
