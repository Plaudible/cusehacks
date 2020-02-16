from PIL import Image
import requests
from io import BytesIO
import urllib.request
#import numpy as np
from face import get_face
from random import uniform
from random import randint
import time

contrast_low = 20
contrast_high = 200

brightness_low = -.15
brightness_high = .15

noise_low = 0
noise_high = .4

eye = Image.open('eye.png').convert("RGBA")
eye_width, eye_height = eye.size

def readIMG(url):
    return Image.open(urllib.request.urlopen(url))

def getIMG(path):
    return Image.open(path).convert("RGBA")

def place(img,points):
    eye_temp = eye
    for (x,y,r) in points:
        img.paste(eye,(x-int(eye_width/2),y-int(eye_height/2)),eye)
    return img

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

def noise(img,lvl=uniform(noise_low, noise_high)):
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
    img = brightness(img,lvl=brightness_high-.2)
    img = contrast(img,lvl=contrast_high)
    img = noise(img)
    return img

if __name__ == "__main__":
    url = 'https://i.imgur.com/26Hs09m.jpg'
    path = 'g.jpeg'
    l = get_face(path)
    print(l)
    t0 = time.time()
    img = place(getIMG(path),l)
    img = fry(img)
    t1 = time.time()
    img.save('out4.png')
    print('Time to out: ', t1-t0)

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
    # img = getIMG('yeet.jpg')
    # img = brightness(img,-.20)
    # img = contrast(img,contrast_high+100)
    # img = noise(img,.4)
    # # img = sharpen(img)
    # # img.save('out'+str(a.index(i))+'.png')
    # # print(type(img))
    # img.save('out2.png')