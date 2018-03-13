#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################################
# Communication with sound level meter TENMA 72-947
# Script : soundMeter.py
#
# Communication serial entre Arduino et Raspberry
# Protocol :
#  - Emettre "M" pour demander les mesures
#  - Recevoir un entier entre 0 et 1023 suivit de \r\n
#  - 9600bps, 8, 1, n, n
######################################################

import serial
import time


ser = serial.Serial('COM23', 9600)
time.sleep(1)   #on attend un peu, pour que l'Arduino soit prêt.    
ser.write(119)
ser.close()

#while 1:
#    
#    lecture = ser.read()
#    lecture = ord(lecture)
# #   print(lecture) #on affiche la reponse
#    if (lecture == 165):
#        lecture = ser.read()
#        lecture = ord(lecture)
##        print(lecture) #on affiche la reponse
#        if (lecture == 13):
#            dat = ser.read(2)
#            dat = map(ord, dat)
#            sound = dat[0]*10+dat[1]*0.1
#            print (sound) 
##3            time.sleep(1)
   