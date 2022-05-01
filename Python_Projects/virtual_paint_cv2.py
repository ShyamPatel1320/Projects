import cv2
from matplotlib.pyplot import contour
import numpy as np
cm = cv2.VideoCapture(0) #webcam default 0
cm.set(3,640)#(id,frame width)
cm.set(4,480)#(id,frame height)
cm.set(10,150)
#value from object detection Trackbar
myColors = [[113,48,0,179,255,255]]#pink
            # [104,126,0,115,212,162], #blue color [min,min,min,max,max,max]
            # [0,57,64,20,255,255],#skin
            # [0,99,97,61,139,255],#red
            # [21,75,0,29,255,255],#ye color
            # [35,0,0,179,24,85]#black
            # ,[20,0,9,104,23,97],#white
            # [57,76,0,100,255,255]]#green
            # ] #skin color(hand,face)

myColorsValue = [[127,0,255]]#pink   BGR format
                # [255,0,0], #blue
                # [153,153,255],#skin
                # [0,0,255],#red
                # [0,255,255],#yellow
                # [0,0,0],#black
                # [255,255,255],#white
                # [0,255,0]]#green

myPoints = [] #[x,y,colorid] colorid = mycolorvalue if 0 then 255,0,0

def findColor(img,myColors,myColorsValue):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    c=0 #for getting color values
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3]) #lower = np.array([h_min,s_min,v_min])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getcontours(mask) #store center value
        cv2.circle(imgResult,(x,y),10,myColorsValue[c],cv2.FILLED) #display circle at returned value point
        if x!=0 and y!=0:
            newPoints.append([x,y,c])
        c+=1
        # cv2.imshow(str(color[0]),mask) #3 output window is generated,in each iteration we changed show window name if we put it same then only last values window we get
    return newPoints

def getcontours(img):#Get edge value of shape
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#find shape
    x,y,w,h = 0,0,0,0 # if area<500 then return 0
    for cnt in contours:
        area = cv2.contourArea(cnt) #find area
        if area>500: #shape area >500 then run
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),2)#draw shape border
            peri = cv2.arcLength(cnt,True) #find arc points
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)#round value of arc points
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y # return center of top edge

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorsValue[point[2]],cv2.FILLED)

while True:
    success,img = cm.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorsValue)
    if len(newPoints) != 0:
        for npt in newPoints: #we get newPoint as list so we can't put it inside list
            myPoints.append(npt) #append each point
    if len(myPoints) != 0:
        drawOnCanvas(myPoints,myColorsValue)
    cv2.imshow("Result",imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break