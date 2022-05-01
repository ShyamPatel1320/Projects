import random #generate random values
import sys
from pip import main #for exit the programme
import pygame
from pygame.locals import *
pygame.init() #initialize all pygame module
import cv2
import numpy as np
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
surface = pygame.display.set_mode([511,300])
cap = cv2.VideoCapture(0)
FPS = 32
SCREENWIDTH = 315
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprits/bird.png'
BACKGROUND = 'sprits/background.png'
PIPE = 'sprits/pipe.png'
def isCollide(playerx , playery , upperpipes , lowerpipes ):
    if playery > GROUNDY-29 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerpipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
def getRandompipe():
    """ generate position of 2 pipes"""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.6*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipeX,'y': -y1}, # upper pipe y negative
        {'x':pipeX,'y': y2} # lower pipe 
    ]
    return pipe
def maingame():
    """ main game working"""
    score=0
    newPipe1 = getRandompipe()
    newPipe2 = getRandompipe()
    #list of upper pipe
    upperpipes = [
        {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y': newPipe2[0]['y']},
    ]
    #list of lower pipe
    lowerpipes = [
        {'x': SCREENWIDTH+200 , 'y' : newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y' : newPipe2[1]['y']},
    ]
    pipeVelX = -9 #pipe speed
    myColors = [[113,48,0,179,255,255]]#pink color
                # [0,57,64,20,255,255]] #skin color(hand,face)

    myColorsValue = [[255,0,0]]
                    # [153,153,255]]

    myPoints = [] #[x,y,colorid] colorid = mycolorvalue if 0 then 255,0,0

    def findColor(frame,myColors,myColorsValue):
        imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        c=0 #for getting color values
        newPoints = []
        for color in myColors:
            lower = np.array(color[0:3]) #lower = np.array([h_min,s_min,v_min])
            upper = np.array(color[3:6])
            mask = cv2.inRange(imgHSV,lower,upper)
            x,y = getcontours(mask) #store center value
            cv2.circle(frame,(x,y),10,myColorsValue[c],cv2.FILLED) #display circle at returned value point
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
                cv2.drawContours(frame,cnt,-1,(255,0,0),2)#draw shape border
                peri = cv2.arcLength(cnt,True) #find arc points
                approx = cv2.approxPolyDP(cnt,0.02*peri,True)#round value of arc points
                x,y,w,h = cv2.boundingRect(approx)
        return x+w//2,y # return center of top edge

    while True:
        success, frame = cap.read()
        newPoints = findColor(frame,myColors,myColorsValue)
        if len(newPoints) != 0:
            for npt in newPoints: #we get newPoint as list so we can't put it inside list
                myPoints.append(npt) #append each point
        playerx = newPoints[0][0]
        playery = newPoints[0][1]
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
      
        crashTest = isCollide(playerx , playery , upperpipes , lowerpipes ) # this function return true if player crashed
        if crashTest:
            return

        #moves pipe to left

        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX
        # add new pipe
        if 0<upperpipes[0]['x']<10:
            newpipe =getRandompipe()
            upperpipes.append(newpipe[0])    
            lowerpipes.append(newpipe[1])    
            score+=1
            GAME_SOUNDS['wing'].play()


        
        #if pipe out of screen then remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        
        #blit the sprites during game
        surface.fill([0,0,0])

        #for some reasons the frames appeared inverted
        frame = np.fliplr(frame)
        frame = np.rot90(frame)
        # The video uses BGR colors and PyGame needs RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surf = pygame.surfarray.make_surface(frame)
        pygame.display.flip()
        surface.blit(surf, (0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            surface.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            surface.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        # surface.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        surface.blit(GAME_SPRITES['player'],(newPoints[0][0],newPoints[0][1]))
        #show our score

        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            surface.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def home():
    width = 415
    height = 566
    z = [width,height]
    white = (255, 255, 255)
    screen_display = pygame.display
    screen_display.set_caption('Game')
    surface = screen_display.set_mode(z)
    python = pygame.image.load('sprits/home.png')
    
    window = True
    while window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window = False
            if event.type==KEYDOWN and (event.key==K_e or event.key==K_UP):
                return
        surface.fill(white)
        surface.blit(python,(50, 50))
        screen_display.update()  
    pygame.quit()
if __name__ == '__main__':
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Game With Shyam Patel')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('sprits/0.png').convert_alpha(),#convert_alpha = work with pixel and alphas 
        pygame.image.load('sprits/1.png').convert_alpha(),#convert = only work with pixel
        pygame.image.load('sprits/2.png').convert_alpha(),
        pygame.image.load('sprits/3.png').convert_alpha(),
        pygame.image.load('sprits/4.png').convert_alpha(),
        pygame.image.load('sprits/5.png').convert_alpha(),
        pygame.image.load('sprits/6.png').convert_alpha(),
        pygame.image.load('sprits/7.png').convert_alpha(),
        pygame.image.load('sprits/8.png').convert_alpha(),
        pygame.image.load('sprits/9.png').convert_alpha()
    )
    GAME_SPRITES['message'] = pygame.image.load('sprits/home.png').convert_alpha()#home page display
    GAME_SPRITES['base'] = pygame.image.load('sprits/base.png').convert_alpha()#base set
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180), # 2 pipe 1 rotate and 2nd strate pipe
        pygame.image.load(PIPE).convert_alpha()
    )

    #GAME SOUNDS SET

    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('audio/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.mp3')

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    while True:
        home()
        maingame()
    


#cv2 webcame in pygame screen
# while True:
#     surface.fill([0,0,0])
#     success, frame = cap.read()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     #for some reasons the frames appeared inverted
#     frame = np.fliplr(frame)
#     frame = np.rot90(frame)
#     # The video uses BGR colors and PyGame needs RGB
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     surf = pygame.surfarray.make_surface(frame)
#     # Show the PyGame surface!
#     surface.blit(surf, (0,0))
#     pygame.display.flip()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break