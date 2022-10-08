########## Imports ##########
import pathlib
import sys, os
from PIL import Image
import pydicom as dicom
from PyQt5 import QtCore, QtGui, QtWidgets,uic
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from GUI import Ui_MainWindow
import matplotlib.pyplot as plt

#! --------------------------------------------------------------------------------------------------------------------------------------------------- #

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI.ui', self)
        self.show()

        #?######### Links of GUI Elements to Methods ##########

        self.pushButton.clicked.connect(self.openImage)

#! ------------------------------------------------------------------------------------------------------------------------------------------------ #


#?### Main Methods ####

    # Browse and get image path then call a specific function according to image format
    def openImage(self):
        print('0')
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','c:/', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
        imagePath = fileName[0]
        if pathlib.Path(imagePath).suffix == ".jpg":
            self.jpgFormat(imagePath)
        elif pathlib.Path(imagePath).suffix == ".bmp":
            self.bmpFormat(imagePath)
        elif pathlib.Path(imagePath).suffix == ".dcm":
            self.dicomFormat(imagePath)
    
    # View jpg image format and show its attributes
    def jpgFormat(self, imagePath):
        print('jpg')
        image = Image.open(imagePath)
        self.viewImage(imagePath)
        self.nuberOfRowsResultLable.setText(f'{image.width}')
        self.numberOfColumnsResultLable.setText(f'{image.height}')
        self.imageColorResultLable.setText(f'{image.mode}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        # self.bitDepthResultLable.setText(f'{image.depth}')

    # View bmp image format and show its attributes
    def bmpFormat(self, imagePath):
        print('bmp')
        image = Image.open(imagePath)
        self.viewImage(imagePath)
        self.nuberOfRowsResultLable.setText(f'{image.width}')
        self.numberOfColumnsResultLable.setText(f'{image.height}')
        self.imageColorResultLable.setText(f'{image.mode}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        # self.bitDepthResultLable.setText(f'{image.depth}')

    # View DICOM image format and show its attributes 
    def dicomFormat(self, imagePath):
        print('dicom')
        image = dicom.dcmread(imagePath)
        self.patientNameResultLable.setText(f'{image.PatientName}')
        self.modalityResultLable.setText(f'{image.Modality}')
        self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
        self.patientAgeResultLable.setText(f'{image.PatientAge}')
        self.nuberOfRowsResultLable.setText(f'{image.Rows}')
        self.numberOfColumnsResultLable.setText(f'{image.Columns}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        # self.bitDepthResultLable.setText(f'{image.depth}')
        # self.imageColorResultLable.setText(f'{image.mode}')

    # Helper function to view jpg and bmp image formate
    def viewImage(self, imagePath):
        pix = QPixmap(imagePath)
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.imageGraphicsView.setScene(scene)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()