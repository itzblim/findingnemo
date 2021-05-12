import pytesseract
import cv2
import numpy as np
from PIL import Image
from pytesseract import Output
import re


input_text = "express"
# Step 1: Image Cleaning
# Greyscale, blahblah


# def image_cleaning(image):
#     grey = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
#     remove_noise = cv2.medianBlur(grey, 5)
#     return remove_noise


img = cv2.imread('psle.png')
# img = image_cleaning(img)
search_result = input_text.lower()

d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        if re.match(search_result, d['text'][i].lower()):
            (x, y, w, h) = (d['left'][i], d['top']
                            [i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


cv2.namedWindow('img', cv2.WINDOW_NORMAL)
# resize window dependent on size of original window?
# or should window not be displayed at all
# (i.e. just use the x,y,w,h values to demarcate where to place the box on the actual webpage image itself)
cv2.resizeWindow('img', 600, 600)

cv2.imshow('img', img)
cv2.waitKey(0)

# print(pytesseract.image_to_string(img))


# language setting somewhere along the way
# search terms to be boxed (test if can search date without the regex)

# manage multiple images
# resizing for multiple images
# https://stackoverflow.com/questions/55915217/providing-big-40173007-image-to-cv2-imshow-does-not-display-the-whole-image

# https://nanonets.com/blog/ocr-with-tesseract/

# seems to be some bug with the reading of "6"
