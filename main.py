#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class rsa(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        
        self.setupUi(self)
        
        self.codeButton.clicked.connect(self.code)
        self.decodeButton.clicked.connect(self.decode)
    
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = rsa()
    window.show()
    sys.exit(app.exec_())