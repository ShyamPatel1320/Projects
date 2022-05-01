import random #generate random values
import sys #for exit the programme
import pygame
from pygame.locals import *
pygame.init() #initialize all pygame module

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'sprits/bird.png'
BACKGROUND = 'sprits/background.png'
PIPE = 'sprits/pipe.png'

def welcomescreen():
    playerx = int((SCREENWIDTH)/5)# set bird x axis location
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2) # set bird y axis location
    messagex= int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN) and (event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_e or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex , GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def maingame():
    """ main game working"""
    score=0
    playerx = int(SCREENWIDTH/5) #set bird in center
    playery = int(SCREENWIDTH/2)
    basex=0
    #create pipes
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

    playerVelY =-4 #come down valocity
    playermaxVelY = 10 # max height for bird
    playerminVelY = -8 # min height for bird
    playerAccY =1

    while True:
        playerflapAccv = -9 # velocity while flapping
        playerflapped = False # it is true only when bird is flapping
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key == K_e or event.key == K_UP):
                if playery>basex:
                    playerVelY=playerflapAccv
                    playerflapped =True
                    GAME_SOUNDS['swoosh'].play()
        
        crashTest = isCollide(playerx , playery , upperpipes , lowerpipes ) # this function return true if player crashed
        if crashTest:
            return
 
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2 
            if pipeMidPos <= playerMidPos < pipeMidPos+4: #my error
               score+=1
               GAME_SOUNDS['wing'].play()
        
        if playerVelY < playermaxVelY and not playerflapped:
            playerVelY += playerAccY

        if playerflapped:
            playerflapped:False
        
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY , GROUNDY - playery - playerHeight)

        #moves pipe to left

        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX
        # add new pipe
        if 0<upperpipes[0]['x']<5:
            newpipe =getRandompipe()
            upperpipes.append(newpipe[0])    
            lowerpipes.append(newpipe[1])    
        
        
        #if pipe out of screen then remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        
        #blit the sprites during game

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe,lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        #show our score

        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
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
    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipeX,'y': -y1}, # upper pipe y negative
        {'x':pipeX,'y': y2} # lower pipe 
    ]
    return pipe


if __name__ == '__main__':
    FPSCLOCK = pygame.time.Clock() #for control game FPS
    
    #GAME SCREEN DESIGN

    pygame.display.set_caption('Game With Shyam Patel')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('sprits/0.png').convert_alpha(), #convert_alpha = work with pixel and alphas 
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
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    while True:
        welcomescreen()
        maingame()