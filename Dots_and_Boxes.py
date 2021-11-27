#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 09:07:51 2021

@author: eliasmuller
"""

#import the necessary libraries 
#note that if the code is run for the first time pygame must be installed using:

#pip install pygame
import pygame
import sys
import numpy as np
import math
from random import randrange as rand

pygame.init() #the pygame library is initiated and ready to be used

class Lines_Boxes:
    
    def __init__(self, w = 400, h = 400, boxes = 8, screen = None): #using interchangable variables to allow for later changes in the setup

        self.wid = w #width of the window
        self.hei = h #hight of the window
        self.boxes = boxes
        self.len = w // boxes
        self.x = [x*50 for x in range(1, self.boxes)]
        self.y = [x*50 for x in range(1, self.boxes)]
        self.screen = screen

    def _draw_lines(self, color = (100,100,100)): #the draw display method is run every time the Window class is initiated 
        
        x = 0  # Keeps track of the current x to draw the gridlines
        y = 0  # Keeps track of the current y to draw the gridlines    
        for l in range(int(self.wid/self.len)+1):  # We draw one vertical and one horizontal line each loop
            x = x + self.len
            y = y + self.len
            pygame.draw.line(self.screen, color, (x,self.len),(x,self.wid-self.len))
            pygame.draw.line(self.screen, color, (self.len,y),(self.wid-self.len,y))
        pygame.display.update()
        return self.screen
    
    def draw_boxes(self, x_cor, y_cor):

        size_h = self.hei // self.tiles
        size_w = self.wid // self.tiles

        pygame.draw.rect(self.screen, (255, 50, 50), pygame.Rect((self.px * x_cor + 1, self.px * y_cor + 1),
                                                                 (size_w - 0.1, size_h - 0.1)))
        pygame.display.update()
    
    def closestvalue(lst, value):
        arr = np.asarray(lst)
        return(np.abs(arr - value)).argmin()
    
    def colorline_process(self, color = (237,28,36), xcor = 0, ycor = 0, dictio = None):
        xarr = np.asarray(self.x)
        ix = np.abs(xarr - xcor).argmin()
        xclose = xarr[ix]
        yarr = np.asarray(self.y)
        iy = np.abs(yarr - ycor).argmin()
        yclose = yarr[iy]
        print(xclose, yclose)
        
        if xclose == xcor and yclose == ycor:
            pass
        else:
            if xclose == xcor:
                if ycor < yclose:
                    xcor = xcor - 1
                else:
                    xcor = xcor + 1
         
            if yclose == ycor:
                if xcor < xclose:
                    ycor = ycor - 1
                else:
                    ycor = ycor + 1     
    
            if xclose < xcor and yclose < ycor:
                if abs(xcor-(self.len)*round(xclose/(self.len))) > abs(ycor-(self.len)*round(yclose/(self.len))):
                    xclose1, yclose1 = xclose + self.len, yclose 
                else:
                    xclose1, yclose1 = xclose, yclose + self.len
            elif xclose < xcor and yclose > ycor:
                if abs(xcor-(self.len)*round(xclose/(self.len))) > abs(ycor-(self.len)*round(yclose/(self.len))):
                    xclose1, yclose1 = xclose + self.len, yclose 
                else:
                    xclose1, yclose1 = xclose, yclose - self.len
            elif xclose > xcor and yclose > ycor:
                if abs(xcor-(self.len)*round(xclose/(self.len))) > abs(ycor-(self.len)*round(yclose/(self.len))):
                    xclose1, yclose1 = xclose - self.len, yclose 
                else:
                    xclose1, yclose1 = xclose, yclose - self.len
            elif xclose > xcor and yclose < ycor:
                if abs(xcor-(self.len)*round(xclose/(self.len))) > abs(ycor-(self.len)*round(yclose/(self.len))):
                    xclose1, yclose1 = xclose - self.len, yclose 
                else:
                    xclose1, yclose1 = xclose, yclose + self.len
        if 0 not in [xclose, yclose, xclose1, yclose1] and self.wid not in [xclose, yclose, xclose1, yclose1]: #any/ all func did not work
            print([xclose, yclose, xclose1, yclose1])
            if ((xclose, yclose), (xclose1, yclose1)) not in dictio.values(): 
                global count 
                
                dictio[count] = ((xclose, yclose), (xclose1, yclose1))
                dictio[count+.1] = ((xclose1, yclose1), (xclose, yclose))

                count += 1
    
                pygame.draw.line(self.screen, color, (xclose,yclose), (xclose1, yclose1), 3)
                pygame.display.update()
        

            
def main():
    
    value = 400 #the game winow must be quadratic 
    screen = pygame.display.set_mode((value, value))
    pygame.display.set_caption('Dots and Boxes')
    screen.fill((250,250,250))
    pygame.display.update()
    
    filled_lines = {}
    
    clock = pygame.time.Clock()
    Lines_Boxes(screen = screen)._draw_lines()
    crashed = False
    global count
    count = 0

    while not crashed: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                print(mousex, mousey)
                if count%2 == 0: color = (237,28,36)
                if count%2 != 0: color = (0,0,255)
                
                Lines_Boxes(screen = screen).colorline_process(color = color, xcor = mousex, ycor = mousey, dictio = filled_lines)
                print(filled_lines)
                
            print(event)
    
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()        

if __name__ == "__main__" :
    main()
