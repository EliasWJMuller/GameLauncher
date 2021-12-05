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
     
    def __init__(self, master = None):
         
        super().__init__(master = window)
        self.title("Game Description")
        self.geometry("400x200")
        label = Label(self, text ="Descrption")
        label.pack()

def run():
    os.system('/Users/eliasmuller/Desktop/main_D_and_B.py')
   
        
window = Tk()
canvas = Canvas()
l_titel = Label(window, text="Lets Play", foreground = "dark green", font = "Helvetica 18 bold")
l_titel.place(relx=0.5, rely=0.05, anchor="center")
l_st = Label(window, text="Find a collection of different games below - click on the respecitve buttons to find a description or to PLAY. ", foreground = "black", font = "Helvetica 12 bold")
l_st.place(relx=0.5, rely=0.1, anchor="center")

for i in range(0,800,125):
    canvas.create_line(0,i,600,i, dash = (4,2))
canvas.pack(fill=BOTH, expand=1)

#DOTS AND BOXES
l_titel_DB = Label(window, text="Dots and Boxes", foreground = "Black", font = "Helvetica 16")
l_titel_DB.place(relx=0.5, rely=0.2, anchor="center")

btn1 = Button(window, text="Dots and Boxes Description")
btn1.place(relx=0.3, rely=0.250, anchor=CENTER)
btn1.bind("<Button>", lambda e: NewWindowDescr(window))

btn1_2 = Button(window, text="Play Dots and Boxes", command = lambda: execfile('/Users/eliasmuller/Desktop/main_D_and_B.py'))
btn1_2.place(relx=0.7, rely=0.250, anchor=CENTER)

#CLOSE AND STATS
btn1 = Button(window, text="close")
btn1.place(relx=0.3, rely=0.970, anchor=CENTER)
btn1.bind("<Button>", lambda e: NewWindowDescr(window))

btn1_2 = Button(window, text="stats")
btn1_2.place(relx=0.7, rely=0.970, anchor=CENTER)
btn1_2.bind("<Button>", lambda e: NewWindowRun(window))


window.geometry("600x800+10+10")
window.title('Initiation Window')
mainloop()