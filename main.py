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
    e=0 #bez toho to v encrypt_block řvalo že nemůže najít self.e v RSA
    d=0
    n=0

    def GenerateKeys(self):
        print("Generujeme")
        p = RSA.GeneratePrimes(10**16,(10**17))
        
        q = RSA.GeneratePrimes(10**16,(10**17))
        while(p == q):
            q = RSA.GeneratePrimes(10**16,(10**17))
        
        n = p*q
       
        fi = (p - 1)*(q-1)
       
        e =random.randrange(2,fi)
        g = math.gcd(e,fi)
        while (g != 1):
            e = random.randrange(2,fi)
            g = math.gcd(e,fi)
        
        print(e)
        d = RSA.multiplicativeInverse(e,fi)
        
        self.n = n
        self.e = e
        self.d = d
        #self.d = RSA.modinv(self.e,self.fi)
        
        print("DONE!!!")
        self.keyN.setText(str(self.n))
        self.OUTkeyN.setText(str(self.n))
        self.keyD.setText(str(self.e))
        self.keyD_2.setText(str(self.d))
    
    def GeneratePrimes(fromNumber, toNumber):
        number = random.randrange(fromNumber,toNumber)
        while(not RSA.isPrime(number)):
            number = random.randrange(fromNumber,toNumber)
        
        return number
    def multiplicativeInverse(a, b):
        x = 0
        y = 1
        lx = 1
        ly = 0
        oa = a  # Remember original a/b to remove
        ob = b  # negative values from return results
        while b != 0:
            q = a // b
            (a, b) = (b, a % b)
            (x, lx) = ((lx - (q * x)), x)
            (y, ly) = ((ly - (q * y)), y)
        if lx < 0:
            lx += ob  # If neg wrap modulo orignal b
        if ly < 0:
            ly += oa  # If neg wrap modulo orignal a
        # return a , lx, ly  # Return only positive values
        return lx

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = RSA.egcd(b%a,a)
        return (g, x - (b//a) * y, y)
    
    def isPrime(num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num**0.5)+2, 2):
            if num % n == 0:
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
        c = pow(m,self.e,self.n)
        if c == None: print("NOOOO!")
        print(c)
        return c
    def decrypt_block(self,c):
        m = pow(c,self.e,self.n)
        if m == None: print("Noooo!")
        return m
    def getBlocked(string,size):
        result = []
        for i in range(0,len(string),int(size)):
            block = string[i:i*int(size)]
            print(block)
            biteString = ""
            
            for char in block:
                biteString += str((10-len(str(bin(ord(char)))[2:]))*'0'+(str(bin(ord(char)))[2:]))
                
            result.append(str(int(biteString,2))) 
        return result
    
    def sifrovat(self):
        print("Sifrovat")
        string = self.Input.toPlainText() #doplnit input
        blocked = RSA.getBlocked(string,7)
        result = ''.join(map(lambda x: str(x), str([(( block ** self.e) % self.n) for block in blocked])));
        #result  = ''.join([chr(self.encrypt_block(ord(x))) for x in string])
        self.Output.setText(result)
        # ... Zobrazit result
        
        
    def desifrovat(self):
        print("Desifrovat")
        string = self.Input.toPlainText() # doplnit input
        result  = ''.join([chr(self.decrypt_block(ord(x))) for x in string])
        self.Output.setText(result)
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
