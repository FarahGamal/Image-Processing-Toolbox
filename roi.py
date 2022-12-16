import cv2
import numpy as np
from PIL import Image

 #image_path
img_path="man.jpeg"

openOriginalImage = Image.open(img_path)
img_raw = np.array(openOriginalImage)

#read image
# img_raw = cv2.imread(img_path)
print(type(img_raw))

#select ROI function
roi = cv2.selectROI(img_raw)

#print rectangle points of selected roi
print(roi)

#Crop selected roi from raw image
roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

#show cropped image
cv2.imshow("ROI", roi_cropped)
cv2.imshow("image", img_path)
cv2.imwrite("crop.jpeg",roi_cropped)

#hold window
cv2.waitKey(0)