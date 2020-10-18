#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 13:40:23 2020

@author: myous8
"""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.backends.backend_pdf import PdfPages
import random as rand
import math
from gridbuilder import *


 
#data = np.array([list(range(120))]*160)
# create discrete colormap
#dark gray, white, red, green, light gray
cmap = colors.ListedColormap(['#292929','white', '#EB1717', "#83FF00",  '#9B9898'])


#norm = colors.BoundaryNorm(bounds, cmap.N)

data = np.ones(shape=(120,160))

#set hard to traverse region
def hard_traverse():
    for _ in range(8):
        xcoord = np.random.randint(0,119)
        ycoord = np.random.randint(0,159)
       # print(xcoord, ycoord)
        for x in range(xcoord -15, xcoord +15):
            for y in range(ycoord-15, ycoord+15):
               if(x >= 0 and x < 120 and y >= 0 and y < 160):
                    numrand = np.random.randint(0,3)
                    if numrand == 1:
                        data[x,y] = 4
                        
 
#set blocked cells  
def blocked_cells():             
    for x in range(0,119):
        for y in range(0,159):
            randnum = np.random.randint(0,5)
            if (randnum == 4 and data[x,y] != 4):
                data[x,y] = 0


"""for _ in range(7):
    r1 = np.random.randint(0,5)
    print(r1)    
    if r1 == 1:    
        numrand = np.random.randint(0,119)
        r2 = np.random.randint(0,2)
        for x in range(numrand - 1, numrand):
            for y in range(0, 20):
                a = 0
                b =20
                data[x,y] = 3
                r2 = np.random.randint(0,3)
                if r2 == 0:
                    for x in range(numrand - 1, numrand):
                        for y in range(b, b+20):
                            data[x,y] = 3
                else if r2 ==1:"""
                
                
#pick start point

def start():
    r1 = np.random.randint(0,4)
    print(r1)
    if r1 == 0 :
       r2 = np.random.randint(0,119)
       r3 = np.random.randint(0,19)
       while(data[r2,r3] == 4):
           r2 = np.random.randint(0,119)
           r3 = np.random.randint(0,19)
       data[r2,r3] = 2
    elif r1 == 1:  
       r2 = np.random.randint(0,19)
       r3 = np.random.randint(0,159)
       while(data[r2,r3] == 0):
           r2 = np.random.randint(0,19)
           r3 = np.random.randint(0,159)
       data[r2,r3] = 2
       #print(r2,r3)
    elif r1 == 2:  
       r2 = np.random.randint(100,119)
       r3 = np.random.randint(0,159)
       while(data[r2,r3] == 0):
           r2 = np.random.randint(100,119)
           r3 = np.random.randint(0,159)
       data[r2,r3] = 2  
       #print(r2,r3)
    elif r1 == 3:  
       r2 = np.random.randint(0,119)
       r3 = np.random.randint(140,159)
       #print(r2,r3)
       while(data[r2,r3] == 0):
           r2 = np.random.randint(0,119)
           r3 = np.random.randint(140,159)
       data[r2,r3] = 2
    print(r2,r3)
    p1 = [r2, r3]
    return [r1, r2, r3]                  
            
#pick goal point 
def goal(r1,r2,r3):  
    r4 = np.random.randint(0,4)
    print(r4)
    while r4 == r1:
        r4 = np.random.randint(0,4)
    if r4 == 0:
       r5 = np.random.randint(0,119)
       r6 = np.random.randint(0,19)
       while(data[r5,r6] == 0 or abs(math.hypot(r6 - r3, r5 - r2)) < 100):
           print(abs(math.hypot(r6 - r3, r5 - r2)))
           r5 = np.random.randint(0,119)
           r6 = np.random.randint(0,19)
       data[r5,r6] = 3
    elif r4 == 1:  
       r5 = np.random.randint(0, 19)
       r6 = np.random.randint(0,159)
       while(data[r5,r6] == 0 or abs(math.hypot(r6 - r3, r5 - r2)) < 100):
           print(abs(math.hypot(r6 - r3, r5 - r2)))
           r5 = np.random.randint(0,19)
           r6 = np.random.randint(0,159)
       data[r5,r6] = 3
    elif r4 == 2:  
       r5 = np.random.randint(100,119)
       r6 = np.random.randint(0,159)
       while(data[r5,r6] == 0 or abs(math.hypot(r6 - r3, r5 - r2)) < 100):
           print(abs(math.hypot(r6 - r3, r5 - r2)))
           r5 = np.random.randint(100,119)
           r6 = np.random.randint(0,159)
       data[r5,r6] = 3  
    elif r4 == 3:  
       r5 = np.random.randint(100,119)
       r6 = np.random.randint(140,159)
       while(data[r5,r6] == 0 or abs(math.hypot(r6 - r3, r5 - r2)) < 100):
           print(abs(math.hypot(r6 - r3, r5 - r2)))
           r5 = np.random.randint(0,119)
           r6 = np.random.randint(140,159)
       data[r5,r6] = 3
    print(r5,r6)

load()
hard_traverse()
blocked_cells()
res = start()
r1 = res[0]
r2 = res[1]
r3 = res[2]
goal(r1,r2,r3)
                    
   # bounds = [-0.5,0.5,0.5]
    #norm = colors.BoundaryNorm(bounds, cmap.N, clip = False) 
        
fig, ax = plt.subplots(figsize = (20,20))

#x = np.random.randint(low = 0, high = 160, size = 120)
#y = np.random.randint(low = 0, high = 160, size = 120)
#line, = ax.plot(x, y)


ax.set_xlim(-0.5,159.5)
ax.set_ylim(-0.5,119.5)
ax.xaxis.set_major_locator(MultipleLocator(160.5))
ax.yaxis.set_major_locator(MultipleLocator(120.5))
ax.xaxis.set_minor_locator(AutoMinorLocator(160.5))
ax.yaxis.set_minor_locator(AutoMinorLocator(120.5))
ax.grid(which='major', color='black', linestyle='')
ax.grid(which='minor', color='black', linestyle='--', linewidth = 0.01)
ax.imshow(data, cmap=cmap, origin = 'lower')

# draw gridlines
#ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
#ax.set_xticks(np.arange(0, 100, 100));
#ax.set_yticks(np.arange(0, 100, 100));

num = 1;
for num in range(0,100):
    num+= 1
plt.ion
plt.savefig('mod.pdf')
#plt.show()


  