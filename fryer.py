from PIL import Image
import requests
from io import BytesIO
import urllib.request
from face import get_face
from random import uniform
from random import randint
import time

contrast_low = 120
contrast_high = 259

brightness_low = -.15
brightness_high = .15

noise_low = .1
noise_high = .4

eye = Image.open('eye.png').convert("RGBA")
eye_width, eye_height = eye.size

def readIMG(url):
    '''Takes a direct link to an image and returns a PIL image'''
    return Image.open(urllib.request.urlopen(url))

def downloadFromURL(url,filename='download.png'):
    '''Takes a direct link to an image and saves it locally with the name filename'''
    i = Image.open(urllib.request.urlopen(url))
    i.save(filename)

def getIMG(path):
    '''Takes a local path and returns a PIL image'''
    return Image.open(path).convert("RGBA")

def place(img,points):
    '''Takes a PIL image and list of tuples and pastes eye.png on all points;
    adjusting the size of eye.png according to the radius of the eye'''
    for (x,y,r) in points:
        eye_temp = eye

        # Scale the size of the lens flare based on the radius to cover the eyes
        i = ((21.0*r)/eye_width)
        j = ((21.0*r)/eye_height)
        maxsize = (eye_width*i,eye_height*j)
        eye_temp.thumbnail(maxsize)
        temp_width, temp_height = eye_temp.size

        # We found that face.py consistently puts the center of the eye too far
        # to the left, so we're shifting it a bit to the right to compensate
        img.paste(eye,(x-int(temp_width/2)+30,y-int(temp_height/2)),eye)
    return img

def contrast(img,lvl=randint(contrast_low,contrast_high)):
    '''Takes a PIL image and adds pixel-wise contrast based on the magnitude of lvl
    (suggested lvl range: [20,200]). Returns PIL Image with contrast
    Code modified from Håken Lid (https://stackoverflow.com/users/1977847/h%c3%a5ken-lid)'''
    img.load()
    # Its worth noting that if lvl=259 you will get a divide by zero error so dont do that
    factor = (259 * (lvl + 255)) / (255 * (259 - lvl))
    # wtf???
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)

def noise(img,lvl=uniform(noise_low, noise_high)):
    '''Takes a PIL image and adds random pixel-wise noise
    (suggested lvl range: [0,.4]). Returns the PIL Image with noise'''
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
    '''Takes a PIL Image and brightens it by lvl percent 
    (suggested lvl range: [-.15,-.15]). Returns brightened PIL Image'''
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

def fry(img,bright=None,con=None,noi=None):
    '''Takes a PIL Image and frys it by adding brightness,
    contrast, and noise to the image. Returns the fried PIL Image'''
    if bright is None: img = brightness(img)
    else: img = brightness(img,lvl=bright)
    if con is None: img = contrast(img)
    else: img = contrast(img,lvl=con)
    if noi is None: img = noise(img)
    else: img = noise(img,lvl=noi)
    return img

def doBot(url,filename='frythis.png',bright=None,con=None,noi=None):
    '''Takes a direct image url and outputs a fried PIL Image with
    lens flares on the eyes'''
    img = readIMG(url)
    downloadFromURL(url,filename)
    points = get_face(filename)
    img = place(img,points)
    img = fry(img)
    return img

if __name__ == "__main__":
    # url = 'https://i.imgur.com/26Hs09m.jpg'
    # path = 'g.jpeg'
    # l = get_face(path)
    # print(l)
    # t0 = time.time()
    # img = place(getIMG(path),l)
    # img = fry(img)
    # t1 = time.time()
    # img.save('out4.png')
    # print('Time to out: ', t1-t0)

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
    # bright = brightness_low
    # con = contrast_high
    # noi = noise_high
    # for i in range(250,270):
    #     if i == 259: continue
    #     img = getIMG('g.jpeg')
    #     l = get_face('g.jpeg')
    #     img = place(img,l)
    #     img = fry(img)
    #     img.save('out'+str(i)+'.png')

    img = getIMG('a.jpg')
    l = get_face('a.jpg')
    print(l)
    img = place(img,l)
    img = fry(img)
    img.save('out2.png')
    # img = fry(img,bright=bright,con=con,noi=noi)

    # img = brightness(img,bright)
    # img = contrast(img,con)
    # img = noise(img,noi)
    # img = sharpen(img)
    # img.save('out'+str(a.index(i))+'.png')
    # print(type(img))

    img.save('out2.png')
    