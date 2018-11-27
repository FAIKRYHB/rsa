#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class rsa(QMainWindow, Ui_MainWindow):
    
    mode=True #true sifrovat
    
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
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = rsa()
    window.show()
    sys.exit(app.exec_())