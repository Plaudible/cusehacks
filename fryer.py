from PIL import Image
import requests
from io import BytesIO
import urllib.request
import numpy as np

contrast_low = 20
contrast_high = 200

brightness_low = -.15
brightness_high = .15

noise_low = .5
noise_high = .9

def readIMG(url):
    return Image.open(urllib.request.urlopen(url))

def getIMG(path):
    return Image.open(path).convert("RGBA")

def place(img,points):
    eye = Image.open('C:\\Users\\TheeTimatahee\\Programming\\Python\\CuseHacks2020\\eyes.png').convert("RGBA")
    for (x,y,r) in points:
        img.paste(eye,(x,y),eye)
    return img

from random import randint
def contrast(img,lvl=randint(contrast_low,contrast_high)):
    img.load()
    factor = (259 * (lvl + 255)) / (255 * (259 - lvl))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

# import colorsys
# from PIL import ImageFilter
# def sharpen(img,lvl):
#     pixels = img.getdata()
#     newData = []
#     for pixel in pixels:
#         r,g,b = pixel
#         h,s,v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
#         s = s**lvl
#         newData.append(new_pixel)
#     img.putdata(newData)
#     return img

def noise(img,lvl):
    pixels = img.getdata()
    newData = []
    for pixel in pixels:
        rand1 = randint(-125,125) * lvl
        rand2 = randint(-125,125) * lvl
        rand3 = randint(-125,125) * lvl
        new_pixel = (max(min(int(pixel[0] + rand1),255),0),
                     max(min(int(pixel[1] + rand2),255),0),
                     max(min(int(pixel[2] + rand3),255),0))
        newData.append(new_pixel)
    img.putdata(newData)
    return img

from random import uniform
def brightness(img,lvl=uniform(brightness_low, brightness_high)):
    lvl = float("%.2f" % round(lvl,2))
    pixels = img.getdata()
    newData = []
    multiplier = 1.0 + lvl
    for pixel in pixels:
        new_pixel = (max(min(int(pixel[0] * multiplier),255),0),
                     max(min(int(pixel[1] * multiplier),255),0),
                     max(min(int(pixel[2] * multiplier),255),0))
        newData.append(new_pixel)
    img.putdata(newData)
    return img

def fry(img):
    img = brightness(img)
    img = contrast(img)
    img = noise(img)
    return img

if __name__ == "__main__":
    url = 'https://i.imgur.com/26Hs09m.jpg'
    path = 'C:\\Users\\TheeTimatahee\\Programming\\Python\\CuseHacks2020\\yeet.jpg'
    img = getIMG(path)
    # img = brightness(img,.4)
    # img = contrast(img,high)
    # a=list(range(0, 1, .1))
    # a=[]
    # i=noise_low
    # while(i<noise_high):
    #     a.append(i)
    #     i += .1
    #     i = float("%.2f" % round(i,2))

    # for i in a:
    #     img = noise(img,i)

    # img = brightness(img,-.20)
    # img = contrast(img,contrast_high+100)
    # img = noise(img,.4)
    # img = sharpen(img)
    # img.save('out'+str(a.index(i))+'.png')
    # print(type(img))
    # img.save('out2.png')