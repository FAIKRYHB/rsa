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

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class RSA(QMainWindow, Ui_MainWindow):
    mode=True #true sifrovat
    e=5 #bez toho to v encrypt_block řvalo že nemůže najít self.e v RSA
    d=370620014871916331107721676071309
    n=1853100074359581741778111505468071

    def GenerateKeys(self):
        print("Generujeme")
        p = RSA.GeneratePrimes(10**16,(10**17))
        
        q = RSA.GeneratePrimes(10**16,(10**17))
        while(p == q):
            q = RSA.GeneratePrimes(10**16,(10**17))
        
        n = p*q
       
        fi = (p - 1)*(q-1)
       
        e = RSA.find_e(fi)
        
        
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
    def find_d(phi_n,e):
        k = 1
        mod0 = False
        while not mod0:
            if (k*phi_n+1) % e == 0:
                return (k*phi_n+1) // e
            k+=1

    def find_e(phi_n):
        e = 3
        while True:
            if not math.gcd(e,phi_n) == 1:
                e+=2
            else:
                return e
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


    def encrypt_block(self,m):
        return (pow(m,self.e) % self.n)
    def decrypt_block(self,c):
        result = ""
        m = bin(pow(int(c),self.d) % self.n)[3:]
        size = 10
        for i in range(0,len(m),size):
            endIndex = (i+int(size))
            if len(m) <= (i + int(size)):
                endIndex = len(m)-1
            block = string[i:endIndex]

            result = result+ chr(int(i))
        #if m == None: print("Noooo!")
        return result

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
        string = self.Input.toPlainText() #doplnit input
        blocked = RSA.getBlocked(string,7)
        result = ""
       
        for x in blocked:
            result = result + str(self.encrypt_block(x)) + "\n"
      #  for block in  blocked:
       #     result = result + " " + str((( block ** self.e) % self.n))
        #result = ''.join(map(lambda x: str(x), str([(( block ** self.e) % self.n) for block in blocked])));
        
        self.Output.setText(result)
        # ... Zobrazit result
        
        
    def desifrovat(self):
        print("Desifrovat")
        blocks = self.Input.toPlainText().split("\n") # doplnit input
        result  = ''.join([chr(self.decrypt_block(x)) for x in blocks])
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

        self.keyN.setText(str(self.n))
        self.OUTkeyN.setText(str(self.n))
        self.keyD.setText(str(self.e))
        self.keyD_2.setText(str(self.d))

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
