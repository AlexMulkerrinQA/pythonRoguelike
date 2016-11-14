#!/usr/bin/env python
import sys
write = sys.stdout.write
write("\e[2;30;40mtest\e[m ")

from subprocess import call
import os
w, h = os.popen('stty size', 'r').read().split()
termWidth = int(w)
termHeight = int(h)

def setCursor(x, y):
        call(['echo','-en','\e[0;0H'])
def setForeground(colour):
        call(['echo','-en','\e[38;5;'+str(colour)+'m'])

setCursor(0,0)
setForeground(3)
print w+','+h
for j in range(termHeight-1):
        call(['echo','-n','1234567890'*8])
        print "\n"
#print "\n" *30