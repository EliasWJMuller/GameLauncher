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
import numpy as np
import time

pygame.init() #the pygame library is initiated and ready to be used

class Lines_Boxes:
    
    def __init__(self, w = 400, h = 400, boxes = 8, screen = None, dictio = None): #using interchangable variables to allow for later changes in the setup

        self.wid = w #width of the window
        self.hei = h #hight of the window
        self.boxes = boxes
        self.len = w // boxes
        self.x = [x*self.len for x in range(1, self.boxes)]
        self.y = [x*self.len for x in range(1, self.boxes)]
        self.screen = screen
        self.dictio = dictio

    def _draw_lines(self, color = (100,100,100)):
        
        x = 0  # Keeps track of the current x to draw the gridlines
        y = 0  # Keeps track of the current y to draw the gridlines    
        for l in range(int(self.wid/self.len)-1):  # We draw one vertical and one horizontal line each loop
            x = x + self.len
            y = y + self.len
            pygame.draw.line(self.screen, color, (x,self.len),(x,self.wid-self.len))
            pygame.draw.line(self.screen, color, (self.len,y),(self.wid-self.len,y))
        pygame.display.update()
        return self.screen
    
    def colorline_process(self, color = None, xcor = 0, ycor = 0):
        line_drawn = 0
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
            if ((xclose, yclose), (xclose1, yclose1)) not in self.dictio.values(): 
                global count
                self.dictio[count] = ((xclose, yclose), (xclose1, yclose1))
                self.dictio[count+.1] = ((xclose1, yclose1), (xclose, yclose))
    
                pygame.draw.line(self.screen, color, (xclose,yclose), (xclose1, yclose1), 3)
                pygame.display.update()
                count += 1
                
    def Rect_InGame(self, color = None):
        global count
        global box
        i = count - 1 
        if self.dictio[i][0][0] != self.dictio[i][1][0]:#drawn line is horizontal
            q1_1 = ((self.dictio[i][0][0], self.dictio[i][0][1]-self.len), (self.dictio[i][1][0],self.dictio[i][1][1]-self.len))
            q1_2 = ((self.dictio[i][0][0], self.dictio[i][0][1]), (self.dictio[i][0][0],self.dictio[i][0][1]-self.len))
            q1_3 = (((self.dictio[i][1][0], self.dictio[i][1][1]), (self.dictio[i][1][0],self.dictio[i][1][1]-self.len)))
                    
            q2_1 = ((self.dictio[i][0][0], self.dictio[i][0][1]+self.len), (self.dictio[i][1][0],self.dictio[i][1][1]+self.len))
            q2_2 = ((self.dictio[i][0][0], self.dictio[i][0][1]), (self.dictio[i][0][0],self.dictio[i][0][1]+self.len)) 
            q2_3 = (((self.dictio[i][1][0], self.dictio[i][1][1]), (self.dictio[i][1][0],self.dictio[i][1][1]+self.len)))
            
            if q1_1 in self.dictio.values():
                if q1_2 in self.dictio.values() and q1_3 in self.dictio.values():
                    pygame.draw.rect(self.screen, color, pygame.Rect(min(self.dictio[i][0][0]+self.len/4,self.dictio[i][1][0]+self.len/4),self.dictio[i][0][1]-self.len+self.len/4, self.len/2, self.len/2))                                                                                                                                                 
                    pygame.display.update()
                    box = 1
                    
            if q2_1 in self.dictio.values():

                if q2_2 in self.dictio.values() and q2_3 in self.dictio.values():
                    pygame.draw.rect(self.screen, color, pygame.Rect(min(self.dictio[i][0][0]+self.len/4,self.dictio[i][1][0]+self.len/4),self.dictio[i][0][1]+self.len/4, self.len/2, self.len/2))                                                                                                                                                 
                    pygame.display.update()
                    box = 1
                    
        elif self.dictio[i][0][1] != self.dictio[i][1][1]:#drawn line is vertical
            q1_1 = ((self.dictio[i][0][0], self.dictio[i][0][1]), (self.dictio[i][0][0]-self.len,self.dictio[i][0][1]))
            q1_2 = ((self.dictio[i][1][0], self.dictio[i][1][1]), (self.dictio[i][1][0]-self.len,self.dictio[i][1][1]))
            q1_3 = (((self.dictio[i][0][0]-self.len, self.dictio[i][0][1]), (self.dictio[i][1][0]-self.len,self.dictio[i][1][1])))
                    
            q2_1 = ((self.dictio[i][0][0], self.dictio[i][0][1]), (self.dictio[i][0][0]+self.len,self.dictio[i][0][1]))
            q2_2 = ((self.dictio[i][1][0], self.dictio[i][1][1]), (self.dictio[i][1][0]+self.len,self.dictio[i][1][1]))
            q2_3 = (((self.dictio[i][0][0]+self.len, self.dictio[i][0][1]), (self.dictio[i][1][0]+self.len,self.dictio[i][1][1])))
          
            if q1_1 in self.dictio.values():
                if q1_2 in self.dictio.values() and q1_3 in self.dictio.values():
                    pygame.draw.rect(self.screen, color, pygame.Rect(self.dictio[i][0][0]-self.len+self.len/4,min(self.dictio[i][0][1]+self.len/4,self.dictio[i][1][1]+self.len/4),self.len/2,self.len/2))                                                                                                                                              
                    pygame.display.update()
                    pygame.display.update()
                    box = 1
            
            if q2_1 in self.dictio.values():
                if q2_2 in self.dictio.values() and q2_3 in self.dictio.values():
                    pygame.draw.rect(self.screen, color, pygame.Rect(self.dictio[i][0][0]+self.len/4,min(self.dictio[i][0][1]+self.len/4,self.dictio[i][1][1]+self.len/4),self.len/2,self.len/2))                                                                                                                                                
                    pygame.display.update()
                    pygame.display.update()
                    box = 1

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
    global box
    count = 0
    color = [(237,28,36), (0,0,255)]
    i = 0
    
    while not crashed:
        box = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                print(mousex, mousey)
                
                Lines_Boxes(screen = screen,dictio = filled_lines).colorline_process(color = color[i], xcor = mousex, ycor = mousey)
                Lines_Boxes(screen = screen,dictio = filled_lines).Rect_InGame(color[i])
                pygame.display.update()
                    
                if box == 1:
                    if i == 1:
                        i = 1
                    else:
                        i = 0
                elif box == 0:
                    if i == 1:
                        i = 0
                    else:
                        i = 1
                
                print(filled_lines)
                
            print(event)
    
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()        

if __name__ == "__main__" :
    main()
