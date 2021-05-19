#!/usr/bin/env python
# coding: utf-8

# In[37]:


wd = r'C:\Users\itzbl\Documents\GoogleCloudPlatform\\'
wd


# In[38]:


# import io
# import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\itzbl\Documents\GoogleCloudPlatform\orbital-2021-a77c895bfae6.JSON"

# def detect_text_uri(uri):
#     """Detects text in the file located in Google Cloud Storage or on the Web.
#     """
#     from google.cloud import vision
#     client = vision.ImageAnnotatorClient()
#     image = vision.Image()
#     image.source.image_uri = uri

#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     print('Texts:')

#     for text in texts:
#         print('\n"{}"'.format(text.description))

#         vertices = (['({},{})'.format(vertex.x, vertex.y)
#                     for vertex in text.bounding_poly.vertices])

#         print('bounds: {}'.format(','.join(vertices)))

#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
#     return texts
   
# test = detect_text_uri("http://digitalnativestudios.com/textmeshpro/docs/rich-text/line-indent.png")


# In[25]:


from PIL import Image, ImageColor, ImageDraw, ImageEnhance


# In[45]:


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
img2 = highlight_area(img, cpu_socket_region, 2.5, outline_color=red, outline_width=2)
img2.save('line-indent2.png')
img2.show()  # Display the result.


# In[42]:


os.getcwd()


# In[ ]:


# Use div ids and links to jump to entries.


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




