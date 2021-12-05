#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 01:27:31 2021
@author: eliasmuller
"""
from tkinter import *
from tkinter.ttk import *
import os

class NewWindowDescr(Toplevel):
     
    def __init__(self, master = None, description = None):
         
        super().__init__(master = window)
        self.title("Game Description")
        self.geometry("500x150")
        titel = Label(self, text ="Descrption", font = "Helvetica 16 bold")
        titel.place(relx = 0.5, rely = 0.2, anchor = CENTER)
        descr = Label(self, text = description, font = "Helvetica 12")
        descr.place(relx = 0.5, rely = 0.6, anchor = CENTER)
        
window = Tk()
canvas = Canvas()
wgeox, wgeoy = 600 , 800
l_titel = Label(window, text="Lets Play", foreground = "dark green", font = "Helvetica 18 bold")
l_titel.place(relx=0.5, rely=0.05, anchor="center")
l_st = Label(window, text="Find a collection of different games below - click on the respecitve buttons to find a description or to PLAY. ", foreground = "black", font = "Helvetica 12 bold")
l_st.place(relx=0.5, rely=0.1, anchor="center")

for i in range(0,wgeoy,125):
    canvas.create_line(0,i,wgeox,i, dash = (4,2))
canvas.pack(fill=BOTH, expand=1)

#DOTS AND BOXES
def run_D_B():
    os.system('/Users/eliasmuller/Desktop/main_D_and_B.py')
    
l_titel_DB = Label(window, text="Dots and Boxes (2 Player)", foreground = "Black", font = "Helvetica 16")
l_titel_DB.place(relx=0.5, rely=0.2, anchor="center")

btn1 = Button(window, text="Dots and Boxes Description")
btn1.place(relx=0.3, rely=0.250, anchor=CENTER)
btn1.bind("<Button>", lambda e: NewWindowDescr(window,
                                               "Rules: Players take turns joining two horizontally or vertically adjacent dots\n"
                                               "by a line. To color in, just click on the chosen line. A player that completes\n"
                                               "the fourth side of a square (a box) colors that box and must play again. When\n"
                                               "all boxes have been colored the game ends and the player who has colored more\n"
                                               "boxes wins."))

btn1_2 = Button(window, text="Play Dots and Boxes", command = run_D_B)
btn1_2.place(relx=0.7, rely=0.250, anchor=CENTER)

#CLOSE AND STATS
btn1 = Button(window, text="close")
btn1.place(relx=0.3, rely=0.970, anchor=CENTER)
btn1.bind("<Button>", lambda e: NewWindowDescr(window))

btn1_2 = Button(window, text="stats")
btn1_2.place(relx=0.7, rely=0.970, anchor=CENTER)
btn1_2.bind("<Button>", lambda e: NewWindowRun(window))


window.geometry(str(wgeox)+"x"+str(wgeoy)+"+10+10")
window.resizable(0, 0)
window.title('Initiation Window')
mainloop()
