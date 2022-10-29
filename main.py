########## Imports ##########

import numpy as np
from PIL import Image
import pydicom as dicom
import sys, pathlib, math
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PyQt5 import  QtWidgets,uic
import cv2 as cv
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
        self.generateTLetterPushButton.clicked.connect(self.generateTLetter)

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Main Methods #########
                                              
                                                #?######## Task 1 Functions  #########

    #! Browse and get image path then call a specific function according to image format
    def openImage(self):

        #* Clear Labels
        self.modalityResultLable.clear()
        self.bodyPartExaminedResultLable.clear()
        self.patientAgeResultLable.clear()
        self.widthLable.clear()
        self.heightLable.clear()
        self.bitDepthResultLable.clear()
        self.imageColorResultLable.clear()
        self.patientNameResultLable.clear()
        self.totalSizeResultLable.clear()

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
            if imageShape.ndim == 2: channels = 1
            else: channels = imageShape.shape[-1]

            #* View image on GUI
            plt.imshow(image, cmap=plt.cm.gray)
            self.Canvas.draw()
            
            #* Hide DICM attributes
            self.hideDicomAttribute()

            #* Calculate bit depth
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
            self.totalSizeResultLable.setText(f'{size}')  
        except:
            # Call helper function to show an error message
            self.ShowPopUpMessage("Corrupted Image! Please choose a valid one.")

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Task 2 Functions  #########

    #! Open image and disply it on the GUI
    def openImageZoomTab(self):

        try:    
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
            #* If image is jpg or jpeg or bmp
            if (pathlib.Path(imagePath).suffix == ".jpg") or (pathlib.Path(imagePath).suffix == ".bmp") or (pathlib.Path(imagePath).suffix == ".jpeg"):
                
                #* Try and except to handdel corrupted image
                try:
                    #* Open image
                    self.image = Image.open(imagePath)
                    #* Convert image to 2D array
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

                    #* Get width and height from image attributes 
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

                    #* Get width and height from image attributes 
                    self.oldImageWidth = self.image.Rows
                    self.oldImageHeight = self.image.Columns

                    #* Display dimension of the image
                    self.originalWH.setText(str(self.oldImageWidth) + str(' x ') + str(self.oldImageHeight))
                except:

                    #* Show Error message
                    self.ShowPopUpMessage("Corrupted Image! Please choose a valid one")
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")

    #! Call functions of interpolation to make zoom    
    def zoom(self):

        try:
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
                self.nearestInterpolation(newImageHeight, newImageWidth, factor, newImageArray)

                #* Call this function to convert 2D array to an image then display it
                self.convertArrayToImagePolt(newImageArray, self.nearestLabel, self.nearestWH)

                #* Call Bilinear function 
                newImageArray = self.bilinearInterpolation(self.imageArray, self.oldImageWidth, self.oldImageHeight, newImageArray, newImageWidth, newImageHeight)

                #* Call this function to convert 2D array to an image then display it
                self.convertArrayToImagePolt(newImageArray, self.bilinearLabel, self.linearWH)
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")
 
    #! Nearest-neighbor Interpolation function
    #* Take new width and height of new image, factor and new image array
    def nearestInterpolation(self, newImageHeight, newImageWidth, factor, newImageArray):

        try:
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
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")

    #! Bi-linear Interpolation Function
    #* Take old image array, width and height and new image array, width, height
    def bilinearInterpolation(self, imageArray, oldImageWidth, oldImageHeight, newImageArray, newImageWidth, newImageHeight):

        try:

            #* Get scaling factors of width and height
            #* Check if the denominator equals 0 or not
            if newImageHeight != 0: scaleFactorWidth = oldImageWidth / newImageWidth
            else: scaleFactorWidth = 0
            if newImageWidth != 0: scaleFactorHeight = oldImageHeight / newImageHeight  
            else: scaleFactorHeight = 0

            #* Loop on new image by two for loops, outer for rows(height) innner for columns(width)
            for i in range(newImageHeight):
                for j in range(newImageWidth):

                    #* Get coordinates by multiply current row/column to the factor scale
                    x = i * scaleFactorHeight
                    y = j * scaleFactorWidth

                    #* Here we get x and y to get 4 pixels arround the point
                    #* We get x, y below this point using floor
                    coordinateXFloor = math.floor(x)
                    coordinateYFloor = math.floor(y)

                    #* We get x, y above this point using ceil, we use min function 
                    #* to make sure it will not be out the original image
                    coordinateXCeil = min(oldImageHeight - 1, math.ceil(x))
                    coordinateYCeil = min(oldImageWidth - 1, math.ceil(y))

                    #* After calculate x, y we have 4 vlues for the 4 surrounding pixels
                    #* here we get its values from the original image 
                    firstPoint = imageArray[coordinateXFloor, coordinateYFloor]
                    secondPoint = imageArray[coordinateXCeil, coordinateYFloor]
                    thirdPoint = imageArray[coordinateXFloor, coordinateYCeil]
                    fourthPoint = imageArray[coordinateXCeil, coordinateYCeil]

                    #* Check for some cases

                    #* If x ceil equals x floor that is mean that x is interger (same for y)
                    #* so we don't need to calculate its pixel value, we get it from the original image
                    if (coordinateXCeil == coordinateXFloor) and (coordinateYCeil == coordinateYFloor):
                        newImageArray[i,j] = imageArray[int(x), int(y)]
                    
                    #* If x ceil equals to x floor so x is interger 
                    #* so we have one value for x 
                    #* it seems like we make linear interpolation along vertical axis
                    elif (coordinateXCeil == coordinateXFloor):
                        firstPixelValue = imageArray[int(x), int(coordinateYFloor)]
                        secondPixelValue = imageArray[int(x), int(coordinateYCeil)]
                        newImageArray[i,j] = firstPixelValue * (coordinateYCeil - y) + secondPixelValue * (y - coordinateYFloor)
                    
                    #* If y ceil equals to y floor so y is interger 
                    #* so we have one value for y 
                    #* it seems like we make linear interpolation along horizontal axis
                    elif (coordinateYCeil == coordinateYFloor):
                        firstPixelValue = imageArray[int(coordinateXFloor), int(y)]
                        secondPixelValue = imageArray[int(coordinateXCeil), int(y)]
                        newImageArray[i,j] = (firstPixelValue * (coordinateXCeil - x)) + (secondPixelValue * (x - coordinateXFloor))
                    
                    #* if not of the above cases found we calculate it by 
                    #* make 2 linear interpolation along vertical and horizontal axis
                    #* then get pixel value
                    else:
                        firstPixelValue = firstPoint * (coordinateXCeil - x) + secondPoint * (x - coordinateXFloor)
                        secondPixelValue = thirdPoint * (coordinateXCeil - x) + fourthPoint * (x - coordinateXFloor)
                        newImageArray[i,j] = firstPixelValue * (coordinateYCeil - y) + secondPixelValue * (y - coordinateYFloor)

            #* After all this calculations this function return array of new image
            return newImageArray
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")

    def interpolationRound(self, val):
        if round(val,1) == 0.5:
            val = int(val)
        else:
            val = round(val)
        return val

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Task 2 Functions  #########
    
    def generateTLetter(self):
        width = 128
        height = 128

        image = (width, height, 3)
        array = np.zeros(image, dtype=np.uint8)

        for i in range(28, 48):
            for j in range(28, 98):
                array[i,j] = [255, 255, 255]

        for i in range(48, 98):
            for j in range(53, 73):
                array[i,j] = [255, 255, 255]

        img = Image.fromarray(array)

        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.tLetterGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        plt.imshow(img, cmap='gray')
        self.Canvas.draw()
        rotatedImage, new_height, new_width, output = self.rotate(array, 80)
        # test = self.bilinearInterpolation(array, 128,128,output,new_width,new_height) 
        # interpolate = Image.fromarray(np.uint8(test))
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        self.rotatedImageGridLayout.addWidget(self.Canvas,0, 0, 1, 1)

        plt.imshow(rotatedImage, cmap='gray')
        self.Canvas.draw()
    
    def shear(self, angle,x,y):
        # shear 1
        tangent=math.tan(angle/2)
        new_x=round(x-y*tangent)
        new_y=y
        #shear 2
        new_y=round(new_x*math.sin(angle)+new_y)      #since there is no change in new_x according to the shear matrix
        #shear 3
        new_x=round(new_x-new_y*tangent)              #since there is no change in new_y according to the shear matrix
        return new_y,new_x

    def rotate(self, image,a): 
    #image : your image
    #a : angle to rotate your image
        angle = - ( a )            
        angle=math.radians(angle)                               
        cosine=math.cos(angle)
        sine=math.sin(angle)
        height=image.shape[0]    
        width=image.shape[1]                                  
        # height and width of the new image 
        new_height  = round(abs(image.shape[0]*cosine)+abs(image.shape[1]*sine))+1
        new_width  = round(abs(image.shape[1]*cosine)+abs(image.shape[0]*sine))+1
        #image variable of dimensions of new_height and new _column filled with zeros
        output=np.zeros((new_height,new_width,image.shape[2]))
        image_copy=output.copy()
        #Find the centre of the image about which we have to rotate the image
        original_centre_height   = round(((image.shape[0]+1)/2)-1)    
        original_centre_width    = round(((image.shape[1]+1)/2)-1)   
        # Find the centre of the new image that will be obtained
        new_centre_height= round(((new_height+1)/2)-1)        
        new_centre_width= round(((new_width+1)/2)-1)          

        for i in range(height):
            for j in range(width):
                #co-ordinates of pixel with respect to the centre of original image
                y=image.shape[0]-1-i-original_centre_height                   
                x=image.shape[1]-1-j-original_centre_width 
                '''
                #co-ordinate of pixel with respect to the rotated image
            
                new_y=round(-x*sine+y*cosine)
                new_x=round(x*cosine+y*sine)
                '''
                
                new_y,new_x = self.shear(angle,x,y)
                new_y=new_centre_height-new_y
                new_x=new_centre_width-new_x
            
                if 0 <= new_x < new_width and 0 <= new_y < new_height and new_x>=0 and new_y>=0:

                    output[new_y,new_x,:]=image[i,j,:] 
        pil_img=Image.fromarray((output).astype(np.uint8))      

        pil_img.save("rotated_image.png")    
        img=cv.imread("rotated_image.png")
        img_2=cv.imread("img.jpg")

        # plt.imshow(img, cmap='gray')
        # plt.imshow(img, cmap='gray')
        # cv.imshow("Befor Rotate",img_2)
        # cv.imshow("After Rotate",img)
        cv.waitKey(0)
        return img, new_height, new_width, output
          
    

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