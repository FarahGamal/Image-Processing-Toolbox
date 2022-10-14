########## Imports ##########

from tkinter import Canvas
from PIL import Image
import sys, os, pathlib
import pydicom as dicom
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from PyQt5 import  QtWidgets,uic
from PyQt5.QtWidgets import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#?-----------------------------------------------------------------------------------------------------------------------------#

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI.ui', self)
        self.setWindowTitle("Image Viewer")
        self.show()

        #?######### Initializations ##########
    
        #* Bit depth dictionary 
        self.imageColorDictionary = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

        self.test()
        #* Canvas definition 
        # self.figure = plt.figure(figsize=(15,5))
        # self.Canvas = FigureCanvas(self.figure)
        # self.gridLayout.addWidget(self.Canvas,0, 0, 1, 1)
        # self.originaImageGridLayout.addWidget(self.Canvas,0, 0, 1, 1)
        # self.nearestNeighborGridLayout.addWidget(self.Canvas,0, 0, 1, 1)
        # self.linearGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        self.lineEdit.setValidator(QIntValidator())
        #!?######### Links of GUI Elements to Methods ##########

        self.browseButton.clicked.connect(self.openImage)

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Main Methods #########

    #! Browse and get image path then call a specific function according to image format
    def openImage(self):

        #* Get image path
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
        imagePath = fileName[0]

        #* Check image format then call its function
        if (pathlib.Path(imagePath).suffix == ".jpg") or (pathlib.Path(imagePath).suffix == ".bmp"):
            self.jpgAndBmpFormat(imagePath)
        elif pathlib.Path(imagePath).suffix == ".dcm":
            self.dicomFormat(imagePath)
    
    #! View jpg and bmp image format and show its attributes
    def jpgAndBmpFormat(self, imagePath):

        # This try and except to handel corrupted image 
        try:
            self.figure = plt.figure(figsize=(15,5))
            self.Canvas = FigureCanvas(self.figure)
            self.gridLayout.addWidget(self.Canvas,0, 0, 1, 1)
            #* Open image then view it in the GUI
            image = Image.open(imagePath)
            plt.imshow(image, cmap=plt.cm.gray)
            self.Canvas.draw()
            # pixmap = QPixmap(imagePath)
            # item = QtWidgets.QGraphicsPixmapItem(pixmap)
            # scene = QtWidgets.QGraphicsScene(self)
            # scene.addItem(item)
            # self.graphicsView.setScene(scene)
            
            #* Hide DICM attributes
            self.hideDicomAttribute()

            #* Show attributes of the image
            self.heightLable.setText(f'{image.height}')
            self.widthLable.setText(f'{image.width}')
            self.imageColorResultLable.setText(f'{image.mode}')
            self.totalSizeResultLable.setText(f'{8*(os.path.getsize(imagePath))}')
            self.bitDepthResultLable.setText(f'{self.imageColorDictionary[image.mode]}')
        except:
            # Call helper function to show an error message
            self.ShowPopUpMessage("Can not open this file.")

    #! View DICOM image format and show its attributes 
    def dicomFormat(self, imagePath):

        # This try and except to handel corrupted image 
        try:
            self.figure = plt.figure(figsize=(15,5))
            self.Canvas = FigureCanvas(self.figure)
            self.gridLayout.addWidget(self.Canvas,0, 0, 1, 1)
            
            #* Open image then view it 
            image = dicom.dcmread(imagePath)
            plt.imshow(image.pixel_array,cmap=plt.cm.gray)
            self.Canvas.draw()

            # scene = QtWidgets.QGraphicsScene(self)
            # self.scene = scene
            # figure = Figure()
            # axes = figure.gca()
            # axes.get_xaxis().set_visible(False)
            # axes.get_yaxis().set_visible(False)
            # axes.imshow(image.pixel_array, cmap=plot.cm.bone)
            # canvas = FigureCanvas(figure)
            # canvas.setGeometry(0, 0, 500, 500)
            # scene.addWidget(canvas)
            # self.graphicsView.setScene(scene)
            
            #* Show DICM attributes
            self.showDicomAttribute()

            #* Show attributes of the image
            if hasattr(image, 'Modality'): self.modalityResultLable.setText(f'{image.Modality}')
            else : self.modalityResultLable.setText('------')
            if hasattr(image, 'StudyDescription'): self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
            else : self.bodyPartExaminedResultLable.setText('------')
            if hasattr(image, 'PatientAge'): self.patientAgeResultLable.setText(f'{image.PatientAge}')
            else : self.patientAgeResultLable.setText('------')
            if hasattr(image, 'Rows'): self.widthLable.setText(f'{image.Rows}')
            else : self.widthLable.setText('------')
            if hasattr(image, 'Columns'): self.heightLable.setText(f'{image.Columns}')
            else : self.heightLable.setText('------')
            if hasattr(image, 'BitsAllocated'): self.bitDepthResultLable.setText(f'{image.BitsAllocated}')
            else : self.bitDepthResultLable.setText('------')
            if hasattr(image, 'PhotometricInterpretation'): self.imageColorResultLable.setText(f'{image.PhotometricInterpretation}')
            else : self.imageColorResultLable.setText('------')
            if hasattr(image, 'PatientName'): self.patientNameResultLable.setText(f'{image.PatientName}')
            else : self.patientNameResultLable.setText('------')
            self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')  
        except:
            # Call helper function to show an error message
            self.ShowPopUpMessage("Can not open this file.")

    def test(self):
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.originaImageGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.nearestNeighborGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.linearGridLayout.addWidget(self.Canvas,0, 0, 1, 1)
#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Helper Functions #########

    #! Hide all the attributes of the DICM image
    def hideDicomAttribute(self):
        self.patientNameResultLable.hide()
        self.modalityResultLable.hide()
        self.bodyPartExaminedResultLable.hide()
        self.patientAgeResultLable.hide()
        self.patientNameTitleLable.hide()
        self.modalityTitleLable.hide()
        self.bodyPartExaminedTitleLable.hide()
        self.patientAgeTitleLable.hide()

    #! Show all the attributes of the DICM image
    def showDicomAttribute(self):
        self.patientNameResultLable.show()
        self.modalityResultLable.show()
        self.bodyPartExaminedResultLable.show()
        self.patientAgeResultLable.show()
        self.patientNameTitleLable.show()
        self.modalityTitleLable.show()
        self.bodyPartExaminedTitleLable.show()
        self.patientAgeTitleLable.show()

    #! Show an Error Message for Handling Invalid files
    def ShowPopUpMessage(self, popUpMessage):
        messageBoxElement = QMessageBox()
        messageBoxElement.setWindowTitle("ERROR")
        messageBoxElement.setText(popUpMessage)
        execute = messageBoxElement.exec_()

#?-----------------------------------------------------------------------------------------------------------------------------#

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()