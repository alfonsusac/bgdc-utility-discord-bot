from os import listdir
from os.path import isfile, join, splitext
from PIL import Image
import pytesseract
import json
import re
import numpy as np
import string

imagedir = listdir('./data/mokou')
# print(imagedir)
# print(pytesseract.get_languages(config=''))

imagetext = {}

print(pytesseract.image_to_string(Image.open('./data/mokoutext/1.jpg'),lang='eng'))

for i in range(len(imagedir)):
    # # Cropping the images
    # print(i)
    # rawimage = Image.open('./data/mokou/'+imagedir[i])
    # rawdata = np.array(rawimage)
    # converted = np.where(rawdata == 255,255,10)
    # rawimage = Image.fromarray(converted.astype('uint8'))
    # crop image by half
    # w, h = rawimage.size
    # rawimage.crop((0,h*3/4,w,h)).convert('L').save('./data/mokoutext/'+imagedir[i])

    # Detecting Characters
    rawtext = pytesseract.image_to_string('./data/mokoutext/'+imagedir[i],lang='chi_sim').split('\n')
    # print(rawtext)
    engtext = ""
    firstline = True
    for text in rawtext:
        # print(text)
        if not re.search(u'[\u4e00-\u9fff\x0c]',text):
            # print('found:',text)
            if firstline:
                engtext = text
                firstline = False
            else:
                engtext = engtext + text
    delchars = r"-'..?、[~…!,，()]+“_=<>/””"
    engtextprocessed = engtext.lower().translate({ord(c): None for c in (string.whitespace+delchars)}).replace('|','i').replace('1','i')
    # engtextprocessed2 = engtextprocessed.translate({delchars, None})
    
    print(str(i+1), ">>",imagedir[i] , engtextprocessed)
    imagetext[engtextprocessed] = imagedir[i]

with open('./data/mokoutext.json','w') as f:
    json.dump(imagetext, f, indent=4)

print('----')
print(pytesseract.image_to_string(Image.open('./data/mokoutext/1.jpg'),lang='eng'))
print('----')
print(pytesseract.image_to_string(Image.open('./data/mokoutext/1.jpg'),lang='chi_sim'))
# print('----')
# print(pytesseract.image_to_boxes(Image.open('./data/mokoutext/1.jpg')))
