import cv2
from PIL import Image
import numpy as np

# imgColor = cv2.imread('images/oskar-smethurst-B1GtwanCbiw-unsplash.jpg')
# print(imgColor.shape)
# img_gray = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)
# cv2.imwrite('image.png',img_gray)



img = Image.open('images/sample_640×426.bmp')
img = np.array(img)
print(int(np.amax(img)))
print(int(np.amin(img)))
# img = np.array(img)
# # print(img)
# print(img.shape)
# if img.ndim == 2:
#     channels = 1
#     print("image has 1 channel")
# else:
#     channels = img.shape[-1]
#     print("image has", channels, "channels")
# print(channels)
