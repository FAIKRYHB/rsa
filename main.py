#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## Klíče
# 1. p,q => prvočísla 1*10^16.... 9.9....
# 2. n = p*q
# 3. Fí(n) = (p-1)*(q-1)
# 4. 1 < e < Fi(n) : e X Fi(n)  GCD(e, Fí(n)) == 1
# 5. inverzní modulo e : d => e mod Fí(n) = 1

##  713336501923348429570567355419698
## Šifrování
# OT = 'Ahoj pepo'
# Št = OT^e * mod n
# Ze znaku bin číslo a převést na jedno decimální po 7 znacích

## Dešifrování
# OT = ŠT^d * mod n


# Výstup bude soubor bloků čísel.
import random
import math

from random import randrange

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RSA(QMainWindow, Ui_MainWindow):
    mode=True #true sifrovat
    n = ""
    d = ""
    e = ""
    def GenerateKeys(self):
        keySize = 17
        print("Generujeme")
        p = RSA.GeneratePrimes(keySize)
        
        q = RSA.GeneratePrimes(keySize)
        while(p == q):
            q = RSA.GeneratePrimes(keySize)
        
        n = p*q
       
        fi = (p - 1)*(q-1)
       
        e = random.randrange(1, fi)
        
        
        #print(e)
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

    

    def GeneratePrimes(k):
         #k is the desired bit length
         r = 100*(math.log(k,2)+1) #number of attempts max
         while r>0:
            #randrange is mersenne twister and is completely deterministic
            #unusable for serious crypto purposes
            n = random.randrange(10**(k-1),10**(k))
            r -= 1
            if RSA.isPrime(n) == True:
                return n
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
            lx += ob 
        if ly < 0:
            ly += oa  
        return lx

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = RSA.egcd(b%a,a)
        return (g, x - (b//a) * y, y)
    
    def rabinMiller(n, k=10):
        if n == 2:
                return True
        if not n & 1:
                return False
    
        def check(a, s, d, n):
                x = pow(a, d, n)
                if x == 1:
                        return True
                for i in range(1, s - 1):
                        if x == n - 1:
                                return True
                        x = pow(x, 2, n)
                return x == n - 1
    
        s = 0
        d = n - 1
    
        while d % 2 == 0:
                d >>= 1
                s += 1
    
        for i in range(1, k):
                a = randrange(2, n - 1)
                if not check(a, s, d, n):
                        return False
        return True

    def isPrime(n):
         lowPrimes =   [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                       ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                       ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                       ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                       ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                       ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                       ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                       ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                       ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                       ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
         if (n >= 3):
             if (n&1 != 0):
                 for p in lowPrimes:
                     if (n == p):
                        return True
                     if (n % p == 0):
                         return False
                 return RSA.rabinMiller(n)
         return False

    
    def switchmode(self):
        if self.mode:
            self.SifDesif.setText("Dešifrovat")
            self.label_OutKey.setText("Veřejný klíč")
            self.label_InKey.setText("Soukromý klíč")
            self.label_InDE.setText("d")
            self.label_OutDE.setText("e")
            self.randomKey.setEnabled(False)
            self.mode=False

            self.keyD.setText(str(self.d))
            self.keyD_2.setText(str(self.e))


        else:
            self.SifDesif.setText("Šifrovat")
            self.label_OutKey.setText("Soukromý klíč")
            self.label_InKey.setText("Veřejný klíč")
            self.label_InDE.setText("e")
            self.label_OutDE.setText("d")
            self.randomKey.setEnabled(True)
            self.mode=True

            self.keyD.setText(str(self.e))
            self.keyD_2.setText(str(self.d))

    def getBlocked(string,size):
        result = []
        
        for i in range(0,len(string),int(size)):
            endIndex = (i+int(size))
            
            if len(string) <= (i + int(size)):
                endIndex = len(string)-1
            
            block = string[i:endIndex]
            #print(string[i*int(size):i*int(size)+size])
            biteString = "1"
            
            for char in block:
                biteString = biteString + (10-len(str(bin(ord(char)))[2:]))*'0'+(str(bin(ord(char)))[2:])
           
            if len(biteString) > 0:
                result.append(int(biteString,2)) 
    
        return result
    
    def sifrovat(self):
        print("Sifrovat")
        string = self.Input.toPlainText() 
        cipher = [str(pow(ord(char), self.e, self.n)) for char in string]
        self.Output.setText(" ".join(cipher))        
        
    def desifrovat(self):
        print("Desifrovat")
        inp = self.Input.toPlainText().split(" ")
        plain = [chr(pow(int(char) ,self.d, self.n)) for char in inp]
         
        self.Output.setText("".join(plain))
        
    def run(self):
        if self.mode:
            self.sifrovat()
        else:
            self.desifrovat()
    
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.keyN.setText(str(self.n))
        self.OUTkeyN.setText(str(self.n))
        self.keyD.setText(str(self.e))
        self.keyD_2.setText(str(self.d))

        self.SifDesif.clicked.connect(self.run)
        self.SwitchSifDes.clicked.connect(self.switchmode)
        self.randomKey.clicked.connect(self.GenerateKeys)
    
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)



    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSA()
    window.show()
    sys.exit(app.exec_())
