########## Imports ##########

from tkinter import Canvas
from PIL import Image
import sys, os, pathlib, magic
import pydicom as dicom
import matplotlib.pyplot as plt
from PyQt5 import  QtWidgets,uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI.ui', self)
        self.show()

        #?######### Initializations ##########

        #* Bit depth dictionary 
        self.imageColorDictionary = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

        #* Canvas definition 
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        #!?######### Links of GUI Elements to Methods ##########

        self.pushButton.clicked.connect(self.openImage)



#?### Main Methods ####

    #! Browse and get image path then call a specific function according to image format
    def openImage(self):
        print('0')

        #* Get image path
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm *.png)")
        imagePath = fileName[0]
        #* Check image format then call its function
        magic.from_file(imagePath)
        if magic.from_file(imagePath) == 'DICOM medical imaging data':
            self.dicomFormat(imagePath)
        else: self.jpgAndBmpFormat(imagePath)
    
    #! View jpg and bmp image format and show its attributes
    def jpgAndBmpFormat(self, imagePath):

        #* Open image then view it 
        image = Image.open(imagePath)
        plt.imshow(image)
        self.Canvas.draw()

        #* Hide DICM attribute
        self.hideDicomAttribute()

        #* Show attributes of the image
        self.nuberOfRowsResultLable.setText(f'{image.width}')
        self.numberOfColumnsResultLable.setText(f'{image.height}')
        self.imageColorResultLable.setText(f'{image.mode}')
        self.totalSizeResultLable.setText(f'{8*(os.path.getsize(imagePath))}')
        self.bitDepthResultLable.setText(f'{self.imageColorDictionary[image.mode]}')

    #! View DICOM image format and show its attributes 
    def dicomFormat(self, imagePath):
        print('dicom')

        #* Open image then view it 
        image = dicom.dcmread(imagePath)
        plt.imshow(image.pixel_array,cmap=plt.cm.gray)
        self.Canvas.draw()

        #* Show DICM attribute
        self.showDicomAttribute()

        #* Show attributes of the image
        if hasattr(image, 'Modality'): self.modalityResultLable.setText(f'{image.Modality}')
        else : self.modalityResultLable.setText('------')
        if hasattr(image, 'StudyDescription'): self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
        else : self.bodyPartExaminedResultLable.setText('------')
        if hasattr(image, 'PatientAge'): self.patientAgeResultLable.setText(f'{image.PatientAge}')
        else : self.patientAgeResultLable.setText('------')
        if hasattr(image, 'Rows'): self.nuberOfRowsResultLable.setText(f'{image.Rows}')
        else : self.nuberOfRowsResultLable.setText('------')
        if hasattr(image, 'Columns'): self.numberOfColumnsResultLable.setText(f'{image.Columns}')
        else : self.numberOfColumnsResultLable.setText('------')
        if hasattr(image, 'BitsAllocated'): self.bitDepthResultLable.setText(f'{image.BitsAllocated}')
        else : self.bitDepthResultLable.setText('------')
        if hasattr(image, 'PhotometricInterpretation'): self.imageColorResultLable.setText(f'{image.PhotometricInterpretation}')
        else : self.imageColorResultLable.setText('------')
        if hasattr(image, 'PatientName'): self.patientNameResultLable.setText(f'{image.PatientName}')
        else : self.patientNameResultLable.setText('------')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')  

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



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()