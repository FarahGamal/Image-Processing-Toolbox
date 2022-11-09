
from matplotlib import pyplot as plt
import cv2
import numpy as np

my_img = cv2.imread('grayyy.jpg', 0)
equ = cv2.equalizeHist(my_img)
res = np.hstack((my_img, equ))
histr = cv2.calcHist([equ],[0],None,[256],[0,256])
plt.plot(histr)
plt.show()