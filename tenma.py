#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################################
# Communication with sound level meter TENMA 72-947
# Script : soundMeter.py
#
# Communication Protocol :
#
#  - 9600bps, 8, 1, n, n
#  - Recevoir 165;13;dat0,dat1
# Calcul du niveau sonore : dat0*10+dat1*0.1
######################################################

import serial
#import qtimer

import sys
from PyQt4 import Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import QTimer 
import PyQt4.Qwt5 as Qwt
import soundmeterGUI

class MainDialog(QDialog,soundmeterGUI.Ui_Dialog):
    def __init__(self,parent=None):
            super(MainDialog,self).__init__(parent)
            self.setupUi(self)
            self.mesure = False
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.acquerirMesures)
            self.timer.setInterval(200)
            
            self.graph.setTitle("Sound Level")
            self.graph.setAxisTitle(0 ,"Sound Level (dBA)")
            self.graph.setAxisTitle(2 ,"Time (x10ms)")
            self.graph.setAxisScale(2,0,21,0)
            self.graph.setAxisScale(0,0,160,0)
            self.graph.setCanvasBackground(Qt.Qt.white)
            self.curveR = Qwt.QwtPlotCurve("Data Moving Right")
            self.curveR.attach(self.graph)
            pen = Qt.QPen(Qt.Qt.green)
            pen.setWidth(5)
            self.curveR.setPen(pen)
            self.x = range(0,21)
            self.y = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            self.seuil = 60.0
            self.filename = "sound"+str(1)+".csv"
            self.t = 0
             

            
    def demarrerMesure(self):
        self.pbArreter.setEnabled(True)
        self.pbDemarrer.setEnabled(False)        
        self.timer.start()
        self.file = open(self.filename,"w") 
        self.t = 0
        
        
    def arreterMesure(self):
        self.pbDemarrer.setEnabled(True)
        self.pbArreter.setDisabled(True)
        self.timer.stop()
        self.file.close()
        
    def modifierSeuil(self):
        self.seuil = float(self.leSeuil.text())
        self.jauge.setAlarmLevel(self.seuil)
        
    def acquerirMesures(self):  
        i=0  
        max = 0.0
        self.ser = serial.Serial('COM23', 9600)
        self.mesure = True
        
        while i<21:
            lecture = self.ser.read()
            lecture = ord(lecture)
            
            if (lecture == 165):
                lecture = self.ser.read()
                lecture = ord(lecture)
            #        print(lecture) #on affiche la reponse
                if (lecture == 27):
                    self.lblUnite.setText("dbA")
                    self.graph.setAxisTitle(0 ,"Sound Level (dBA)")
                if (lecture == 28):
                    self.lblUnite.setText("dbC")
                    self.graph.setAxisTitle(0 ,"Sound Level (dBC)")
                if (lecture == 13):
                    dat = self.ser.read(2)
                    dat = map(ord, dat)
                    sound = dat[0]*10+dat[1]*0.1
                    self.jauge.setValue(sound)
                    #print (sound)
                    for j in range(len(self.y)-2,-1,-1):
                        self.y[j+1]=self.y[j]
                                
                    self.y[0] = sound
                    if sound>self.seuil:
                        pen = Qt.QPen(Qt.Qt.red)
                        pen.setWidth(5)
                        self.curveR.setPen(pen)
                    else:
                        pen = Qt.QPen(Qt.Qt.green)
                        pen.setWidth(5)
                        self.curveR.setPen(pen)
                    print self.y
                    self.file.write(str(self.t*20+i)+";"+str(sound)+"\n")
                    print "\n"
                    self.curveR.setData(self.x, self.y)
                    self.graph.replot()
                    if sound > max:
                        max=sound
                    i=i+1
                    
        self.ser.close()  
        self.lcdNumber.display(max)
        self.t=self.t+1
        
            
app=QApplication(sys.argv) 
form=MainDialog()
form.show()
app.exec_()
