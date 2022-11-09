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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#?-----------------------------------------------------------------------------------------------------------------------------# 

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GUI2.ui', self)
        self.setWindowTitle("Image Viewer")
        self.show()

        #!?######### Links of GUI Elements to Methods ##########

        self.pushButton.clicked.connect(self.browse)
        self.zoomPushButton.clicked.connect(self.zoom)
        self.shearPushButton.clicked.connect(self.shear)
        self.browseButton.clicked.connect(self.openImage)
        self.nearestPushButton.clicked.connect(self.rotation)
        self.bilinearPushButton.clicked.connect(self.rotation)
        self.shearNegativePushButton.clicked.connect(self.shear)
        self.browsePushButton.clicked.connect(self.openImageZoomTab)
        self.equalizePushButton.clicked.connect(lambda: self.equalizeHistogram(self.gr_img, self.histogram, self.max_depth+1))
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
                newImageWidth = round(factor * self.oldImageWidth)
                newImageHeight = round(factor * self.oldImageHeight) 

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

                    if newRowCoordinate > self.imageArray.shape[0] - 1  or  newColCoordinate > self.imageArray.shape[1] - 1 :
                        #* floor result
                        newRowCoordinateImg = int(np.floor(newRowCoordinate))
                        newColCoordinateImg = int(np.floor(newColCoordinate))
                    else:
                        newRowCoordinateImg = round(newRowCoordinate)
                        newColCoordinateImg = round(newColCoordinate)

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

                                                #?######## Task 3 Functions  #########
    
    #! Generate T letter
    def generateTLetter(self):
        width = 128
        height = 128
        
        # Generate an array of zeros 
        image = (width, height, 3)
        self.array = np.zeros(image, dtype=np.uint8)

        # This two for loops to draw horizontal part of 'T'
        for i in range(28, 48):
            for j in range(28, 98):
                self.array[i,j] = [255, 255, 255]

        # This two for loops to draw vertical part of 'T'
        for i in range(48, 98):
            for j in range(53, 73):
                self.array[i,j] = [255, 255, 255]

        # Convert array to image
        img = Image.fromarray(self.array)

        # Display it on canvas
        self.drawCanvas(img, self.tLetterGridLayout)

    #! Rotation Using Nearest
    def rotation(self):
        try:
            # Clear label
            self.informationLabel.clear()
            # Get angel from spin box
            angle = self.rotateDoubleSpinBox.value()

            # If condition to check direction of rotation and print it in the label
            if angle < 0:
                self.informationLabel.setText(str(abs(angle)) + str(' in Clockwise Direction.'))
            elif angle > 0:
                self.informationLabel.setText(str(abs(angle)) + str(' in Anticlockwise Direction.'))
            else: 
                self.informationLabel.setText(str('No Rotation ! '))

            # Convert angle to radians
            rad = math.radians(angle)
            # Create array of zeros for rotated image
            rotatedImage = np.uint8(np.zeros(self.array.shape))
            # Width and Height of rotated image
            height = rotatedImage.shape[0]
            width = rotatedImage.shape[1]
            # Get center of the image
            centerX, centerY = (width//2, height//2)
            # Loop on rotated image 
            # Height = Row
            # Width = Column
            for i in range(rotatedImage.shape[0]):
                for j in range(rotatedImage.shape[1]):
                    
                    # This if check which interpolation button is clicked
                    # Nearest Interpolation
                    if self.nearestPushButton.isChecked():
                        # Shift point to fixed point which is center
                        # Multiply by rotation matrix
                        x = (i-centerX)*math.cos(rad)+(j-centerY)*math.sin(rad)
                        y = -(i-centerX)*math.sin(rad)+(j-centerY)*math.cos(rad)
                        # Check if x, y out original image
                        # if it out we make int
                        if x > rotatedImage.shape[0] - 1  or  y > rotatedImage.shape[1] - 1 :
                            interpolateX = int(np.floor(x)) 
                            interpolateY = int(np.floor(y))

                        # if it is in original image we make round
                        else:
                            interpolateX = round(x)
                            interpolateY = round(y)
                        
                        # Then we shift it again to its original coordaniates
                        x = interpolateX + centerX
                        y = interpolateY + centerY
                        
                        # Check if the x,y negative or not have pixels in orignal image
                        if (x>=0 and y>=0 and x<self.array.shape[0] and  y<self.array.shape[1]):
                            rotatedImage[i, j] = self.array[x, y]

                    # Bi-linear Interpolation
                    elif self.bilinearPushButton.isChecked():
                        # Shift point to fixed point which is center
                        # Multiply by rotation matrix
                        # Then return it again
                        x = ((i-centerX)*math.cos(rad)+(j-centerY)*math.sin(rad)) + centerX
                        y = (-(i-centerX)*math.sin(rad)+(j-centerY)*math.cos(rad)) + centerY

                        # Here we get x and y to get 4 pixels arround the point
                        # We get x, y below this point using floor
                        coordinateXFloor = math.floor(x) 
                        coordinateYFloor = math.floor(y) 
                        
                        # We get x, y above this point using ceil, we use min function 
                        # to make sure it will not be out the original image
                        coordinateXCeil = min(height - 1, math.ceil(x)) 
                        coordinateYCeil = min(width - 1, math.ceil(y)) 
                        
                        # Here we get four neighbour pixels
                        # we also check x, y are positive 
                        if (coordinateXFloor>=0 and coordinateYFloor>=0 and coordinateXFloor<self.array.shape[0] and  coordinateYFloor<self.array.shape[1]):
                            firstPoint = self.array[coordinateXFloor, coordinateYFloor]
                        if (coordinateXCeil>=0 and coordinateYFloor>=0 and coordinateXCeil<self.array.shape[0] and  coordinateYFloor<self.array.shape[1]):
                            secondPoint = self.array[coordinateXCeil, coordinateYFloor]
                        if (coordinateXFloor>=0 and coordinateYCeil>=0 and coordinateXFloor<self.array.shape[0] and  coordinateYCeil<self.array.shape[1]):
                            thirdPoint = self.array[coordinateXFloor, coordinateYCeil]
                        if (coordinateXCeil>=0 and coordinateYCeil>=0 and coordinateXCeil<self.array.shape[0] and  coordinateYCeil<self.array.shape[1]):
                            fourthPoint = self.array[coordinateXCeil, coordinateYCeil]

                        # Here we check x, y are positive 
                        if (x>=0 and coordinateXCeil>=0 and coordinateXFloor>=0 and y>=0 and coordinateYCeil>=0 and coordinateYFloor>=0 and coordinateXCeil<self.array.shape[0] and coordinateXFloor<self.array.shape[0] and x<self.array.shape[0] and coordinateYCeil<self.array.shape[1] and coordinateYFloor<self.array.shape[1] and y<self.array.shape[1]):
                            
                            # If x ceil equals x floor that is mean that x is interger (same for y)
                            # so we don't need to calculate its pixel value, we get it from the original image
                            if (coordinateXCeil == coordinateXFloor) and (coordinateYCeil == coordinateYFloor):
                                rotatedImage[i,j] = self.array[int(x), int(y)]
                            
                            # If x ceil equals to x floor so x is interger 
                            # so we have one value for x 
                            # it seems like we make linear interpolation along vertical axis
                            elif (coordinateXCeil == coordinateXFloor):
                                firstPixelValue = self.array[int(x), int(coordinateYFloor)]
                                secondPixelValue = self.array[int(x), int(coordinateYCeil)]
                                rotatedImage[i,j] = firstPixelValue * (coordinateYCeil - y) + secondPixelValue * (y - coordinateYFloor)

                            # If y ceil equals to y floor so y is interger 
                            # so we have one value for y 
                            # it seems like we make linear interpolation along horizontal axis
                            elif (coordinateYCeil == coordinateYFloor):
                                firstPixelValue = self.array[int(coordinateXFloor), int(y)]
                                secondPixelValue = self.array[int(coordinateXCeil), int(y)]
                                rotatedImage[i,j] = (firstPixelValue * (coordinateXCeil - x)) + (secondPixelValue * (x - coordinateXFloor))
                            
                            # if not of the above cases found we calculate it by 
                            # make 2 linear interpolation along vertical and horizontal axis
                            # then get pixel value
                            else:
                                firstPixelValue = firstPoint * (coordinateXCeil - x) + secondPoint * (x - coordinateXFloor)
                                secondPixelValue = thirdPoint * (coordinateXCeil - x) + fourthPoint * (x - coordinateXFloor)
                                rotatedImage[i,j] = firstPixelValue * (coordinateYCeil - y) + secondPixelValue * (y - coordinateYFloor)
                
            # return rotatedImage    
            rotatedImage = Image.fromarray(rotatedImage)

            self.drawCanvas(rotatedImage, self.rotatedImageGridLayout)
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")
    
    #! Shear in x direction
    def shear(self):
        try:
            self.informationLabel.clear()
            shearImage = np.uint8(np.zeros(self.array.shape))
            # Width and Height of shear image
            height = shearImage.shape[0]
            width = shearImage.shape[1]
            # Get center of the image
            centerX, centerY = (width//2, height//2)
            # Loop on shear image 
            # Height = Row
            # Width = Column
            for i in range(shearImage.shape[0]):
                for j in range(shearImage.shape[1]):
                    # Shift point to fixed point which is center
                    newX = i - centerX
                    newY = j - centerY

                    # newX = newX
                    # Check which button is clicked
                    if self.shearPushButton.isChecked():
                        newY = newX + newY
                        self.informationLabel.setText(str(' Horizontal Shear 45 Degrees '))

                    elif self.shearNegativePushButton.isChecked():
                        newY = -newX + newY
                        self.informationLabel.setText(str(' Horizontal Shear -45 Degrees '))

                    
                    # Nearest interpolation
                    if newX > shearImage.shape[0] - 1  or  newY > shearImage.shape[1] - 1 :
                        interpolateX = int(np.floor(newX)) 
                        interpolateY = int(np.floor(newY))
                    else:
                        interpolateX = round(newX)
                        interpolateY = round(newY)
                    
                    newX = interpolateX + centerX
                    newY = interpolateY + centerY

                    if (newX>=0 and newY>=0 and newX<self.array.shape[0] and  newY<self.array.shape[1]):
                        shearImage[i, j] = self.array[newX, newY]
            
            # return shear Image    
            shearImage = Image.fromarray(shearImage)

            self.drawCanvas(shearImage, self.rotatedImageGridLayout)
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")

#?-----------------------------------------------------------------------------------------------------------------------------#

                                                #?######## Task 4 Functions  #########
    
    #! Browse image and show the image and its normalized histogram
    def browse(self):
        try:
            #* Clear canvas before draw
            self.clearCanvas(self.OriginalgridLayout)
            self.clearCanvas(self.normalizedGridLayout)
            self.clearCanvas(self.equalizedHistoGridLayout)
            self.clearCanvas(self.equalizedImageGridLayout)

            #* Get image path
            fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image','D:\FALL22\SBEN324\Task#1\Image-Viewer\images', "Image files (*.jpg *.jpeg *.bmp *.dcm)")
            self.imagePath = fileName[0]
            
            #* Check image format
            if (pathlib.Path(self.imagePath).suffix == ".jpg") or (pathlib.Path(self.imagePath).suffix == ".bmp") or (pathlib.Path(self.imagePath).suffix == ".jpeg"):
                #* open image and convert it to array
                image = Image.open(self.imagePath)
                imageShape = np.array(image)
                #* Check if the image grey scale or not 
                if imageShape.ndim == 2 and image.mode == 'L':
                    self.gr_img = imageShape
                    #* Calculate maximum value of pixels
                    max = np.amax(self.gr_img)
                    depth = math.ceil(math.log((int(max) + 1), 2))
                    self.max_depth = 2 ** depth
                    #* Draw original image
                    self.drawCanvas(self.gr_img, self.OriginalgridLayout)
                else:
                    #* Convert to grey scale
                    img = mpimg.imread(self.imagePath)
                    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
                    self.gr_img = 0.2989 * R + 0.587 * G + 0.114 * B
                    #* Calculate maximum value of pixels
                    max = np.amax(self.gr_img)
                    depth = math.ceil(math.log((int(max) + 1), 2))
                    self.max_depth = 2 ** depth
                    #* Draw original image
                    self.drawCanvas(self.gr_img, self.OriginalgridLayout)
                #* Call normalized histogram function to calculate and display it
                self.histogram = self.normalizedHistogram(self.gr_img, self.normalizedGridLayout)
            elif pathlib.Path(self.imagePath).suffix == ".dcm":
                #* Read DICOM image    
                image = dicom.dcmread(self.imagePath)
                #* Convert image 2D array
                self.gr_img = image.pixel_array.astype(int)
                self.gr_img = (np.maximum(self.gr_img, 0) / self.gr_img.max()) * 255.0
                self.gr_img = np.uint8(self.gr_img)
                #* Calculate maximum value of pixels
                max = np.amax(self.gr_img)
                depth = math.ceil(math.log((int(max) + 1), 2))
                self.max_depth = 2 ** depth
                #* Draw original image
                self.drawCanvas(image.pixel_array, self.OriginalgridLayout)
                #* Call normalized histogram function to calculate and display it
                self.histogram = self.normalizedHistogram(self.gr_img, self.normalizedGridLayout)
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")

    #! Calculate Normalized histogram and show it
    def normalizedHistogram(self, image, layout):
        try:
            #* Create array of zeros
            histo = np.zeros(self.max_depth+1)
            #* Loop on 2d array of the image to calculate frequancey of pixel values
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    histo[int(image[i, j])] += 1
            #* Make the array normalized by dividing by size        
            histo /= (image.shape[0] * image.shape[1])
            #* Call histogram function to draw it
            self.drawHistogram(layout, np.arange(len(histo)), histo)
            #* Return array of histogram
            return histo
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")
    
    #! Calculate equalized image and its histogram
    def equalizeHistogram(self, img, histo, L):
        try:
            #* Create an array for equalized histogram and image
            equalizedHistogram = np.zeros_like(histo)
            equalizedImage = np.zeros_like(img)

            #* For loop to calculate cdf and sk
            for i in range(len(histo)):
                equalizedHistogram[i] = round((L - 1) * np.sum(histo[0:i]))
            #* Get equalized image
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    pixel_val = int(img[i, j])
                    equalizedImage[i, j] = equalizedHistogram[pixel_val]
            #* Get and draw equalized histogram
            histogm = self.normalizedHistogram(equalizedImage, self.equalizedHistoGridLayout)
            #* Draw equalized image
            self.drawCanvas(equalizedImage, self.equalizedImageGridLayout)
        except:
            self.ShowPopUpMessage("An ERROR OCCURED!!")
            
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
                                               
                                                #?######## Task 4 Helper Functions  #########
 #! Draw Histogram
    def drawHistogram(self, layout, x, y):
        #* Create a canvas
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        layout.addWidget(self.Canvas,0, 0, 1, 1)

        plt.bar(x, y)
        plt.ylabel('Number of Pixels')
        plt.xlabel('Pixel Value')
        self.Canvas.draw()                                              

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

    #! Draw a Canvas then display an image on it
    def drawCanvas(self, image, layout):

        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        layout.addWidget(self.Canvas,0, 0, 1, 1)

        plt.imshow(image, cmap='gray')
        self.Canvas.draw() 

    #! Clear Canvas
    def clearCanvas(self, layout):
        self.figure = plt.figure(figsize=(15,5))
        self.Canvas = FigureCanvas(self.figure)
        layout.addWidget(self.Canvas,0, 0, 1, 1)


#?-----------------------------------------------------------------------------------------------------------------------------#

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()