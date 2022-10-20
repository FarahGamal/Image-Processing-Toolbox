########## Imports ##########

import numpy as np
import sys, pathlib
from PIL import Image
import pydicom as dicom
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PyQt5 import  QtWidgets,uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#?-----------------------------------------------------------------------------------------------------------------------------# 

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI2.ui', self)
        self.setWindowTitle("Image Viewer")
        self.show()

        #!?######### Links of GUI Elements to Methods ##########

        self.browseButton.clicked.connect(self.openImage)
        self.browsePushButton.clicked.connect(self.openImageZoomTab)
        self.zoomPushButton.clicked.connect(self.zoom)

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Main Methods #########
                                              
                                                #?######## Task 1 Functions  #########

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
            #* Canvas to view image on it
            self.figure = plt.figure(figsize=(15,5))
            self.Canvas = FigureCanvas(self.figure)
            self.gridLayout.addWidget(self.Canvas,0, 0, 1, 1)

            #* Open image then view it in the GUI
            image = Image.open(imagePath)

            #* Get channel number
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
            #* Canvas to view image on it
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

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Task 2 Functions  #########

    #! Open image and disply it on the GUI
    def openImageZoomTab(self):

        #* Clear labels
        self.originalWH.clear()
        self.nearestWH.clear()
        self.linearWH.clear()
        self.nearestLabel.clear()
        self.bilinearLabel.clear()

        #* Draw canvas to display image on it
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.originaImageGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        #* Get image path
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
        imagePath = fileName[0]

        #* Check image format then convert image to 2D array and display it
        #* If it jpg or jpeg or bmp
        if (pathlib.Path(imagePath).suffix == ".jpg") or (pathlib.Path(imagePath).suffix == ".bmp") or (pathlib.Path(imagePath).suffix == ".jpeg"):
            
            #* Try and except to handdel corrupted image
            try:

                #* First we convert image to gray scale
                self.image = Image.open(imagePath)
                imageShape = np.array(self.image)
                
                #* Check if the image grey scale or not 
                if imageShape.ndim == 2 and self.image.mode == 'L':
                    #* Convert image to 2D array
                    self.imageArray = np.asarray(self.image)
                    plt.imshow(self.image, cmap='gray')
                else:
                    #* Convert to grey scale
                    img = mpimg.imread(imagePath)
                    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
                    gray_img = 0.2989 * R + 0.587 * G + 0.114 * B
                    self.imageArray = np.asarray(gray_img)
                    plt.imshow(gray_img, cmap='gray')

                #* plot image on the canvas using pillow 
                self.Canvas.draw()

                #* Get width and height from image atributtes 
                self.oldImageWidth = self.image.width
                self.oldImageHeight = self.image.height

                #* Display dimension of the image
                self.originalWH.setText(str(self.oldImageWidth) + str(' x ') + str(self.oldImageHeight))
            except:

                #* Show Error message
                self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")
        #* If DICOM image
        elif pathlib.Path(imagePath).suffix == ".dcm":

            #* Try and except to handdel corrupted image
            try:

                #* Read DICOM image    
                self.image = dicom.dcmread(imagePath)

                #* Convert image 2D array
                new_image = self.image.pixel_array.astype(float)
                self.imageArray = (np.maximum(new_image, 0) / new_image.max()) * 255.0
                self.imageArray = np.uint8(self.imageArray)
                
                #* plot image on the canvas using pillow  
                plt.imshow(self.image.pixel_array,cmap=plt.cm.gray)
                self.Canvas.draw()

                #* Get width and height from image atributtes 
                self.oldImageWidth = self.image.Rows
                self.oldImageHeight = self.image.Columns

                #* Display dimension of the image
                self.originalWH.setText(str(self.oldImageWidth) + str(' x ') + str(self.oldImageHeight))
            except:

                #* Show Error message
                self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")

    #! Call functions of interpolation to make zoom    
    def zoom(self):

        #* Get zooming factor from user
        factor = self.doubleSpinBox.value()

        #* Check if factor equals to zero show error message else make zoom
        if factor <= 0 :
            self.ShowPopUpMessage("You Can't Zoom By Factor Zero!")
            pass
        else:

            #* Calculate new width and height
            newImageWidth = int(factor * self.oldImageWidth)
            newImageHeight = int(factor * self.oldImageHeight) 

            #* Make an empty 2D array for the zoomed image 
            newImageArray = np.empty([newImageHeight, newImageWidth])

            #* Call Nearest-neighbor function 
            self.interpolationNearest(newImageHeight, newImageWidth, factor, newImageArray)

            #* Call this function to convert 2D array to an image then display it
            self.convertArrayToImagePolt(newImageArray, self.nearestLabel, self.nearestWH)

            #* Call Bilinear function 
            newImageArray = self.interpolateBilinear(self.imageArray, self.oldImageWidth, self.oldImageHeight, newImageArray, newImageWidth, newImageHeight)

            #* Call this function to convert 2D array to an image then display it
            self.convertArrayToImagePolt(newImageArray, self.bilinearLabel, self.linearWH)
        
    #! Nearest-neighbor Interpolation function
    #* Take new width and height of new image, factor and new image array
    def interpolationNearest(self, newImageHeight, newImageWidth, factor, newImageArray):

        #* Loop on new image by two for loops, outer for rows(height) innner for columns(width)
        for i in range(newImageHeight):
            for j in range(newImageWidth):

                #* Get new coordinates the divide coordinate by factor
                newRowCoordinate = i/factor
                newColCoordinate = j/factor

                #* floor result
                newRowCoordinateImg = int(np.floor(newRowCoordinate))
                newColCoordinateImg = int(np.floor(newColCoordinate))

                #* Get the value of the coordinate then insert it in image array
                newImageArray[i, j] = self.imageArray[newRowCoordinateImg, newColCoordinateImg]

        #* After looping on the image we return an array of zoomed image
        return newImageArray

    #! Bi-linear Interpolation Function
    #* Take old image array, width and height and new image array, width, height
    def interpolateBilinear(self, imageArray, oldImageWidth, oldImageHeight, newImageArray, newImageWidth, newImageHeight):
        
        #* Loop on new image by two for loops, outer for rows(height) innner for columns(width)
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
        
        #* After looping on the image we return an array of zoomed image            
        return newImageArray

    
    def interpolationRound(self, val):
        if round(val,1) == 0.5:
            val = int(val)
        else:
            val = round(val)
        return val


#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Helper Functions #########

                                                #?######## Task 1  Helper Functions  #########
                                                
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


                                                #?######## Task 2 Helper Functions  #########

    #! Convert 2D array to image the display it
    #* Take array of new image, label name and layout name
    def convertArrayToImagePolt(self, newImageArray, layout, label):
        #* First clear layout 
        layout.clear()

        #* Convert 2D array to image 
        image = Image.fromarray(np.uint8(newImageArray))
        
        #* Display image on label
        qimg = image.toqpixmap()
        layout.setPixmap(qimg)

        #* Call this function that display dimension of the zoomed image
        self.displayDimension(image, label)

    #! Calculate and Display dimension of image
    #* Take image and label name
    def displayDimension(self, image, label):

        #* Get width and height from image it self
        width = image.width
        height = image.height

        #* Set text of label with width and height
        label.setText(str(width) + str(' x ') + str(height))
                                               

                                                #?######## General Helper Functions  #########

    #! Show an Error Message for Handling Invalid files
    #* Take Error message as a text
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