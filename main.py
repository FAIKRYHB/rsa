#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Klíče
# 1. p,q => prvočísla 1*10^16.... 9.9....
# 2. n = p*q
# 3. Fí(n) = (p-1)*(q-1)
# 4. 1 < e < Fi(n) : e X Fi(n)  GCD(e, Fí(n)) == 1
# 5. inverzní modulo e : d => e mod Fí(n) = 1


## Šifrování
# OT = 'Ahoj pepo'
# Št = OT^e * mod n
# Ze znaku bin číslo a převést na jedno decimální po 7 znacích

## Dešifrování
# OT = ŠT^d * mod n


# Výstup bude soubor bloků čísel.
import random
import math
from fractions import gcd

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RSA(QMainWindow, Ui_MainWindow):
    mode=True #true sifrovat
    
    def GenerateKeys(self):
        self.p = RSA.GeneratePrime(10**16,10**17-1)
        self.q = RSA.GeneratePrime(10**16,10**17-1)
        self.n = self.p*self.q
        self.fi = (self.p - 1)*(self.q-1)
        self.e = 0
        while (gcd(self.e,self.fi) != 1):
            self.e = RSA.GeneratePrime(2,self.fi-1)
        
        self.d = 0
        
        
        
        
    def GeneratePrime(fromNumber,toNumber):
        primes = [i for i in range(fromNumber,toNumber) if RSA.isPrime(i)]
        return random.choice(primes);
    
    def isPrime(n):
        if n % 2 == 0 and n > 2: 
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def switchmode(self):
        if self.mode:
            self.SifDesif.setText("Dešifrovat")
            self.label_InKey.setText("Soukromý klíč")
            self.label_InDE.setText("d")
            self.label_OutDE.setText("e")
            self.randomKey.setEnabled(False)
            self.mode=False
        else:
            self.SifDesif.setText("Šifrovat")
            self.label_OutKey.setText("Veřejný klíč")
            self.label_InDE.setText("e")
            self.label_OutDE.setText("d")
            self.randomKey.setEnabled(True)
            self.mode=True
    
    def run(self):
        if self.mode:
            self.sifrovat
        else:
            self.desifrovat
    
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        
        self.setupUi(self)
        
        self.SifDesif.clicked.connect(self.run)
        self.SwitchSifDes.clicked.connect(self.switchmode)
        self.randomKey.clicked.connect(self.randomisekey)
    
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
    
#rsa = RSA()
#rsa.GenerateKeys()
#print(rsa.p)
#print(rsa.q)
#print(rsa.n)
#print(rsa.fi)
#print(rsa.e)


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSA()
    window.show()
    sys.exit(app.exec_())
