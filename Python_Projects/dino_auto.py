import time
import pyautogui #used for mouse,keyboard auto input
from PIL import Image,ImageGrab # PIL = import pillow , ImageGrab is used for auto take screenshot
from numpy import asarray

# def TakeScreenShot():
#     '''Take screen shot of current screen'''
#     image=ImageGrab.grab().convert('L') # grab image and convert('L') is convert image in black and white form
#     return image

def hit(key):
    pyautogui.keyDown(key)

def isCollide(data):
    ''' if any pixel in image is black at given pointe then return true or else false'''
    for i in range(425,570): #set x axis pixel
        for j in range(770,820):# y axis pixel
            if data[ i , j ] < 100: # color code (r,g,b) , 0 = black ,255=white
                return True
    return False
# def down(data):
#     for i in range(425,570):
#         for j in range(650,780):
#             if data[ i , j ] < 100: # color code (r,g,b) , 0 = black ,255=white
#                 return True
#     return False

if __name__ == '__main__':
    time.sleep(3) # take screenshot after 2 second
    while True:
        image=ImageGrab.grab().convert('L') # grab image and convert('L') is convert image in black and white form
        data = image.load() # .load() gives pixels of that image 
        if isCollide(data):
            hit("up")
        # if down(data):
        #     hit('down')
        
        # print(data)# gives , image in generate form
        # print(asarray(image)) # gives ,  image in array form asarray convert in array form 

        # ---------------create block for trees detection

        # for i in range(425,570): #set x axis pixel
        #     for j in range(800,850):  # y axis pixel
        #         data[i,j] = 200 # color code (r,g,b) , 0 = black ,255=white
        # for i in range(495,600):
        #     for j in range(650,780):
        #         data[i,j] = 200
        # image.show() # display image
        # break

    
