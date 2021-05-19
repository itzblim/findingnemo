from PIL import Image, ImageColor, ImageDraw, ImageEnhance
from google.cloud import vision
import io
import os


# Imports the Google Cloud client library
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"orbitalvenv\orbital-2021-e0c3d2610d4e.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()


def detect_text_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts


# print(detect_text_uri("http://www.channelnewsasia.com/image/13479570/0x0/1920/2650/471023eb651dabd857528bea473331a3/qV/infographic--how-secondary-school-posting-works-al-cop.png"))


def highlight_area(img, region, factor, outline_color=None, outline_width=1):
    """ Highlight specified rectangular region of image by `factor` with an
        optional colored  boarder drawn around its edges and return the result.
    """
    img = img.copy()  # Avoid changing original image.
    img_crop = img.crop(region)

    brightner = ImageEnhance.Brightness(img_crop)
    img_crop = brightner.enhance(factor)

    img.paste(img_crop, region)

    return img


    # (412,302),(544,304),(543,349),(411,347)
img = Image.open('line-indent.png')

red = ImageColor.getrgb('red')
cpu_socket_region = 412, 302, 544, 348
img2 = highlight_area(img, cpu_socket_region, 2.5,
                      outline_color=red, outline_width=2)
img2.save('line-indent2.png')
img2.show()  # Display the result.


os.getcwd()


# Use div ids and links to jump to entries.

