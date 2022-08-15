from os import listdir
from os.path import isfile, join, splitext
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import json
import re
import numpy as np
import string

imagedir = listdir('./data/mokou')
# print(imagedir)
# print(pytesseract.get_languages(config=''))

imagetext = {}

ListPanitia = [
    'Chalifa Sophie Anggit Andamari',
    'Kevin Phoenix',
    'Aileen',
    'Christopher Fendika Lee',
    'Alfonsus Ardani Chendrawan',
    'I Putu Raka Natha Nugraha',
    'Nayra Jannatri',
    'Hosea Aldri',
    'Vincent Luwardy Wijaya',
    'Jason Paulus',
    'Muhammad Rifqi Adam',
    'Albert Lucky',
    'Robertus Eric',
    'Jouza Muhammad Akbar Pahlawan',
    'Vito Sebastian Sanjaya',
    'Nicholas Tandinata',
    'Dimas Rizky Hutama',
    'Richard Prayogi',
    'Rionaldi Marhanson Wijaya',
    'Hubertus Darrel Santoso',
    'Steven Yoshell Yapriadi',
    'Justin Christian',
    'Bryan Christopher',
    'Ferry',
    'Ahmad Zemar Alvaro',
    'Brian Ferdinand K',
    'Muhammad Maulana Dzikrulloh',
    'Edyth Novian Putra',
    'Dheanandri'
]
ListPanitiaH2L = [
    'Hosea Aldri',
    'Linggaprastha Ammar Ghazy Indyasena',
    'Hary Subroto',
]

# print(pytesseract.image_to_string(Image.open('./data/mokoutext/1.jpg'),lang='eng'))

for i in ListPanitia:

    # Creating New Canvas
    W = 500
    H = 500

    # Get new blank red canvas
    img = Image.new("RGB", (W, H), (212, 63, 67))
    img.save(f"./data/profpic/{i}.png", "PNG")

    # Initialise Drawing Utilities
    draw = ImageDraw.Draw(img)
    # Get font
    font = ImageFont.truetype(r'.\data\Righteous-Regular.ttf', size=300)

    # Get message
    message = ''.join(w[0].upper() for w in i.split())
    message = message[0:2]

    # Get Font Size in pixel
    w, h = draw.textsize(message, font=font)

    # Set font position
    pos = ((W-w)/2,(H-h)/2-40)

    # Set font color
    color = 'rgb(255,255,255)'

    # Draw font
    draw.text(pos,message,fill=color,font=font)
    img.save(f"./data/profpic/{i}.png", "PNG")

for i in ListPanitiaH2L:
    
    # Creating New Canvas
    W = 500
    H = 500

    # Get new blank red canvas
    img = Image.new("RGB", (W, H), (255, 255, 255))
    img.save(f"./data/profpic/{i}.png", "PNG")

    # Initialise Drawing Utilities
    draw = ImageDraw.Draw(img)
    # Get font
    font = ImageFont.truetype(r'.\data\Righteous-Regular.ttf', size=300)

    # Get message
    message = ''.join(w[0].upper() for w in i.split())
    message = message[0:2]

    # Get Font Size in pixel
    w, h = draw.textsize(message, font=font)

    # Set font position
    pos = ((W-w)/2,(H-h)/2-40)

    # Set font color
    color = 'rgb(218,165,40)'

    # Draw font
    draw.text(pos,message,fill=color,font=font)
    img.save(f"./data/profpic/{i}.png", "PNG")