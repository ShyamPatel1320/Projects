
# import pygame module
import  pygame
  
pygame.init()
width = 680
height = 480
z = [width,height]
white = (255, 255, 255)
screen_display = pygame.display
screen_display.set_caption('GEEKSFORGEEKS')
surface = screen_display.set_mode(z)
python = pygame.image.load('sprits/home.png')
  
window = True
while window:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window = False
    surface.fill(white)
    surface.blit(python,(50, 50))
    screen_display.update()  
pygame.quit()