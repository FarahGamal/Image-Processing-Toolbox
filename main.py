########## Imports ##########

from PIL import Image
import sys, os, pathlib
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
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
        imagePath = fileName[0]

        #* Check image format then call its function
        if pathlib.Path(imagePath).suffix == ".jpg":
            self.jpgFormat(imagePath)
        elif pathlib.Path(imagePath).suffix == ".bmp":
            self.bmpFormat(imagePath)
        elif pathlib.Path(imagePath).suffix == ".dcm":
            self.dicomFormat(imagePath)
    
    #! View jpg image format and show its attributes
    def jpgFormat(self, imagePath):
        print('jpg')

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

    #! View bmp image format and show its attributes
    def bmpFormat(self, imagePath):
        print('bmp')

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
        self.bitDepthResultLable.setText(f'{self.imageColorDictionary[image.mode]}') ###

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
        self.patientNameResultLable.setText(f'{image.PatientName}')
        self.modalityResultLable.setText(f'{image.Modality}')
        self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
        self.patientAgeResultLable.setText(f'{image.PatientAge}')
        self.nuberOfRowsResultLable.setText(f'{image.Rows}')
        self.numberOfColumnsResultLable.setText(f'{image.Columns}')
        self.totalSizeResultLable.setText(f'{os.path.getsize(imagePath)}')  ###
        self.bitDepthResultLable.setText(f'{image.BitsAllocated}')
        self.imageColorResultLable.setText(f'{image.PhotometricInterpretation}')

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