########## Imports ##########

import numpy as np
import sys, pathlib
from PIL import Image
import pydicom as dicom
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from PyQt5 import  QtWidgets,uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#?-----------------------------------------------------------------------------------------------------------------------------# 

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI2.ui', self)
        self.setWindowTitle("Image Viewer")
        self.show()

        #?######### Initializations ##########


        #!?######### Links of GUI Elements to Methods ##########

        self.browseButton.clicked.connect(self.openImage)
        self.browsePushButton.clicked.connect(self.openImageZoomTab)
        self.zoomPushButton.clicked.connect(self.zoom)

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
            image = Image.open(imagePath).convert('L')

            #* Converting RGB image to grey scale
            imageShape = np.array(image)
            if imageShape.ndim == 2:
                channels = 1
                print("image has 1 channel")
            else:
                channels = imageShape.shape[-1]
                print("image has", channels, "channels")

            #* View image on GUI
            plt.imshow(image, cmap=plt.cm.gray)
            self.Canvas.draw()
            
            #* Hide DICM attributes
            self.hideDicomAttribute()

            #* Calculate bit depth
            print(int(np.amax(imageShape)))
            print(int(np.amin(imageShape)))
            bitDepth =  (np.ceil(np.log2((int(np.amax(imageShape)))-(int(np.amin(imageShape)))+1))) * channels

            #* Calculate total size
            totalSize = image.height * image.width * bitDepth

            #* Show attributes of the image
            self.heightLable.setText(f'{image.height}')
            self.widthLable.setText(f'{image.width}')
            self.imageColorResultLable.setText(f'{image.mode}')
            self.totalSizeResultLable.setText(f'{totalSize}')
            self.bitDepthResultLable.setText(f'{bitDepth}')
        except:
            # Call helper function to show an error message
            self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")

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
            
            #* Show DICM attributes
            self.showDicomAttribute()

            #* Image total size
            size = image.Rows * image.Columns * image.BitsAllocated

            #* Show attributes of the image
            if hasattr(image, 'Modality'): self.modalityResultLable.setText(f'{image.Modality}')
            else : self.modalityResultLable.setText('------')
            if hasattr(image, 'StudyDescription'): self.bodyPartExaminedResultLable.setText(f'{image.StudyDescription}')
            else : self.bodyPartExaminedResultLable.setText('------')
            if hasattr(image, 'PatientAge'): self.patientAgeResultLable.setText(f'{image.PatientAge}')
            else : self.patientAgeResultLable.setText('------')
            if hasattr(image, 'Rows'): self.oldImageWidthLable.setText(f'{image.Rows}')
            else : self.oldImageWidthLable.setText('------')
            if hasattr(image, 'Columns'): self.oldImageHeightLable.setText(f'{image.Columns}')
            else : self.oldImageHeightLable.setText('------')
            if hasattr(image, 'BitsAllocated'): self.bitDepthResultLable.setText(f'{image.BitsAllocated}')
            else : self.bitDepthResultLable.setText('------')
            if hasattr(image, 'PhotometricInterpretation'): self.imageColorResultLable.setText(f'{image.PhotometricInterpretation}')
            else : self.imageColorResultLable.setText('------')
            if hasattr(image, 'PatientName'): self.patientNameResultLable.setText(f'{image.PatientName}')
            else : self.patientNameResultLable.setText('------')
            self.totalSizeResultLable.setText(f'{size}')  
        except:
            # Call helper function to show an error message
            self.ShowPopUpMessage("Corrupted Image! Please choose a valid one.")

############################################################################################

    def openImageZoomTab(self):

        #* Get image path
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
        imagePath = fileName[0]

        #* Check image format then call its function
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.originaImageGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        #* Check image format then call its function
        if (pathlib.Path(imagePath).suffix == ".jpg") or (pathlib.Path(imagePath).suffix == ".bmp") or (pathlib.Path(imagePath).suffix == ".jpeg"):
    
            try:
                self.image = Image.open(imagePath).convert('L')
                plt.imshow(self.image, cmap=plt.cm.gray)
                self.imageArray = np.asarray(self.image)
                self.oldImageWidth = self.image.width
                self.oldImageHeight = self.image.height
                self.Canvas.draw()
                self.originalWH.setText(str(self.oldImageWidth) + str(' x ') + str(self.oldImageHeight))
            except:
                self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")
        elif pathlib.Path(imagePath).suffix == ".dcm":
            
            try:
                self.image = dicom.dcmread(imagePath)
                new_image = self.image.pixel_array.astype(float)
                self.imageArray = (np.maximum(new_image, 0) / new_image.max()) * 255.0
                self.imageArray = np.uint8(self.imageArray)
                final_image = Image.fromarray(self.imageArray)
                self.oldImageWidth = self.image.Rows
                self.oldImageHeight = self.image.Columns 
                plt.imshow(self.image.pixel_array,cmap=plt.cm.gray)
                self.Canvas.draw()
                self.originalWH.setText(str(self.oldImageWidth) + str(' x ') + str(self.oldImageHeight))
            except:
                self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")
        
    def zoom(self):

        factor = self.doubleSpinBox.value()
        if factor == 0 :
            self.ShowPopUpMessage("You Can't Zoom By Factor Zero!")
            pass
        else:
            newImageWidth = int(factor * self.oldImageWidth)
            newImageHeight = int(factor * self.oldImageHeight) 

            newImageArray = np.empty([newImageHeight, newImageWidth])

            self.interpolationNearest(newImageHeight, newImageWidth, factor, newImageArray)
            self.convertArrayToImagePolt(newImageArray, self.nearestLabel)
            self.nearestWH.setText(str(newImageWidth) + str(' x ') + str(newImageHeight))

            newImageArray = self.interpolateBilinear(self.imageArray, self.oldImageWidth, self.oldImageHeight, newImageArray, newImageWidth, newImageHeight)
            self.convertArrayToImagePolt(newImageArray, self.bilinearLabel)
            self.linearWH.setText(str(newImageWidth) + str(' x ') + str(newImageHeight))

    def interpolationNearest(self, newImageHeight, newImageWidth, factor, newImageArray):

        for i in range(newImageHeight):
            for j in range(newImageWidth):
                newrow = i/factor
                newcol = j/factor
                newrowImg = int(np.floor(newrow))
                newcolImg = int(np.floor(newcol))
                newImageArray[i, j] = self.imageArray[newrowImg, newcolImg]

        return newImageArray

    def interpolateBilinear(self, imageArray, oldImageWidth, oldImageHeight, newImageArray, newImageWidth, newImageHeight):

        for i in range(newImageHeight):
            for j in range(newImageWidth):
                # Relative coordinates of the pixel in output space
                x_out = j / newImageWidth
                y_out = i / newImageHeight

                # Corresponding absolute coordinates of the pixel in input space
                x_in = (x_out * oldImageWidth)
                y_in = (y_out * oldImageHeight)

                # Nearest neighbours coordinates in input space
                x_prev = int(np.floor(x_in))
                x_next = x_prev + 1
                y_prev = int(np.floor(y_in))
                y_next = y_prev + 1

                # Sanitize bounds - no need to check for < 0
                x_prev = min(x_prev, oldImageWidth - 1)
                x_next = min(x_next, oldImageWidth - 1)
                y_prev = min(y_prev, oldImageHeight - 1)
                y_next = min(y_next, oldImageHeight - 1)
                
                # Distances between neighbour nodes in input space
                Dy_next = y_next - y_in
                Dy_prev = 1. - Dy_next # because next - prev = 1
                Dx_next = x_next - x_in
                Dx_prev = 1. - Dx_next # because next - prev = 1
            
                # Interpolate over 3 RGB layers
                newImageArray[i][j] = Dy_prev * (imageArray[y_next][x_prev] * Dx_next + imageArray[y_next][x_next] * Dx_prev) \
                    + Dy_next * (imageArray[y_prev][x_prev]* Dx_next + imageArray[y_prev][x_next] * Dx_prev)
                    
        return newImageArray

    def convertArrayToImagePolt(self, newImageArray, layout):

        im = Image.fromarray(np.uint8(newImageArray))
        qimg = im.toqpixmap()
        layout.clear()
        layout.setPixmap(qimg)

    def interpolationRound(self, val):
        if round(val,1) == 0.5:
            val = int(val)
        else:
            val = round(val)
        return val

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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(popUpMessage)
        msg.setWindowTitle("Error")
        msg.exec_()

#?-----------------------------------------------------------------------------------------------------------------------------#

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()