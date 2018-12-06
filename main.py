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

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RSA(QMainWindow, Ui_MainWindow):
    mode=True #true sifrovat
    

    def GenerateKeys(self):
        print("Generaujeme")
        self.p = RSA.GeneratePrimes(pow(10,16),pow(10,17)-1)
        
        self.q = RSA.GeneratePrimes(pow(10,16),pow(10,17)-1)
        while(self.p == self.q):
            self.q = RSA.GeneratePrimes(pow(10,16),pow(10,17)-1)
        
        self.n = self.p*self.q
       
        self.fi = (self.p - 1)*(self.q-1)
       
        self.e =random.randint(2,self.fi-1)
        while (math.gcd(self.e,self.fi) != 1):
            
            self.e = random.randint(2,self.fi-1)
        
        self.d = RSA.modinv(self.e,self.fi)
        
        print("DONE!!!")
        print(self.n)
        print(self.d)
       self.keyN.setText(str(self.n))
        self.OUTkeyN.setText(str(self.n))
        self.keyD.setText(str(self.e))
        self.keyD_2.setText(str(self.d))
    
    def GeneratePrimes(fromNumber, toNumber):
        number = random.randint(fromNumber,toNumber)
        while(not RSA.isPrime(number)):
            number = random.randint(fromNumber,toNumber)
        
        return number
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = RSA.egcd(b%a,a)
        return (g, x - (b//a) * y, y)

    def modinv(a, m):
        g, x, y = RSA.egcd(a, m)
        if g != 1:
            raise Exception('No modular inverse')
        return x%m
    
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
            self.label_OutKey.setText("Veřejný klíč")
            self.label_InKey.setText("Soukromý klíč")
            self.label_InDE.setText("d")
            self.label_OutDE.setText("e")
            self.randomKey.setEnabled(False)
            self.mode=False
        else:
            self.SifDesif.setText("Šifrovat")
            self.label_OutKey.setText("Soukromý klíč")
            self.label_InKey.setText("Veřejný klíč")
            self.label_InDE.setText("e")
            self.label_OutDE.setText("d")
            self.randomKey.setEnabled(True)
            self.mode=True
    def encrypt_block(self,m):
        print(m)
        print(self.e)
        print(self.n)
        c = self.modinv(pow(m,self.e),self.n)
        if c == None: print("NOOOO!")
        print(c)
        return c
    def decrypt_block(self,c):
        m = self.modinv(pow(c,self.e),self.n)
        if m == None: print("Noooo!")
        return m
    
    def sifrovat(self):
        print("Sifrovat")
        string = "String" #doplnit input
        result  = ''.join([chr(self.encrypt_block(ord(x))) for x in string])
       
        # ... Zobrazit result
        
        
    def desifrovat(self):
        print("Desifrovat")
        string = "Something" # doplnit input
         result  = ''.join([chr(self.decrypt_block(ord(x))) for x in string])
         # ... Zobrazit result
        
    def run(self):
        if self.mode:
            self.sifrovat()
        else:
            self.desifrovat()
    
    
    def __init__(self):
       QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
       self.setupUi(self)
        
        self.SifDesif.clicked.connect(self.run)
        self.SwitchSifDes.clicked.connect(self.switchmode)
        self.randomKey.clicked.connect(self.GenerateKeys)
    
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        #self.GenerateKeys()
        #self.sifrovat()
    
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
