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

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#! -------------------------------------------------------------------------------------------------------------------------------------------------- #


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI.ui', self)

        self.show()

        self.imageColorDictionary = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
        self.imageGraphicsView.hide()
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.gridLayout_2.addWidget(self.Canvas,0, 0, 1, 1)
        #?######### Links of GUI Elements to Methods ##########

        self.pushButton.clicked.connect(self.openImage)



#! ------------------------------------------------------------------------------------------------------------------------------------------------ #


#?### Main Methods ####

    #? Browse and get image path then call a specific function according to image format
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
    
    #? View jpg image format and show its attributes
    def jpgFormat(self, imagePath):
        print('jpg')
        # self.figure = plt.figure(figsize=(15,5))
        # self.Canvas = FigureCanvas(self.figure)
        # self.gridLayout_2.addWidget(self.Canvas,0, 0, 1, 1)

        image = Image.open(imagePath)
        plt.imshow(image)

        self.Canvas.draw()
        
        # self.viewImage(imagePath)
        self.hideDicomAttribute()
        self.nuberOfRowsResultLable.setText(f'{image.width}')
        self.numberOfColumnsResultLable.setText(f'{image.height}')
        self.imageColorResultLable.setText(f'{image.mode}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        self.bitDepthResultLable.setText(f'{self.imageColorDictionary[image.mode]}')

    #? View bmp image format and show its attributes
    def bmpFormat(self, imagePath):
        print('bmp')
        self.Canvas.hide()
        self.imageGraphicsView.show()
        image = Image.open(imagePath)
        self.viewImage(imagePath)
        self.hideDicomAttribute()
        self.nuberOfRowsResultLable.setText(f'{image.width}')
        self.numberOfColumnsResultLable.setText(f'{image.height}')
        self.imageColorResultLable.setText(f'{image.mode}') ###
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        self.bitDepthResultLable.setText(f'{self.imageColorDictionary[image.mode]}') ###

    #? View DICOM image format and show its attributes 
    def dicomFormat(self, imagePath):
        print('dicom')

        self.imageGraphicsView.hide()
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.gridLayout_2.addWidget(self.Canvas,0, 0, 1, 1)

        image = dicom.dcmread(imagePath)
        plt.imshow(image.pixel_array,cmap=plt.cm.gray)

        self.Canvas.draw()

        self.showDicomAttribute()

        self.patientNameResultLable.setText(f'{image.PatientName}')
        self.modalityResultLable.setText(f'{image.Modality}')
        self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
        self.patientAgeResultLable.setText(f'{image.PatientAge}')
        self.nuberOfRowsResultLable.setText(f'{image.Rows}')
        self.numberOfColumnsResultLable.setText(f'{image.Columns}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')
        self.bitDepthResultLable.setText(f'{image.BitsAllocated}')
        self.imageColorResultLable.setText(f'{image.PhotometricInterpretation}')

    #? Helper function to view jpg and bmp image formate
    def viewImage(self, imagePath):
        pix = QPixmap(imagePath)
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.imageGraphicsView.setScene(scene)

    def hideDicomAttribute(self):
        self.patientNameResultLable.hide()
        self.modalityResultLable.hide()
        self.bodyPartExaminedResultLable.hide()
        self.patientAgeResultLable.hide()
        self.patientNameTitleLable.hide()
        self.modalityTitleLable.hide()
        self.bodyPartExaminedTitleLable.hide()
        self.patientAgeTitleLable.hide()

    def showDicomAttribute(self):
        self.patientNameResultLable.show()
        self.modalityResultLable.show()
        self.bodyPartExaminedResultLable.show()
        self.patientAgeResultLable.show()
        self.patientNameTitleLable.show()
        self.modalityTitleLable.show()
        self.bodyPartExaminedTitleLable.show()
        self.patientAgeTitleLable.show()



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()