import cv2
from PIL import Image
import numpy as np

# imgColor = cv2.imread('images/oskar-smethurst-B1GtwanCbiw-unsplash.jpg')
# print(imgColor.shape)
# img_gray = cv2.cvtColor(imgColor, cv2.COLOR_BGR2GRAY)
# cv2.imwrite('image.png',img_gray)



img = Image.open('images/sample_640×426.bmp')
matrix = np.array(img.getdata())
list = list(img.getdata())
print(list)
# print(matrix.size)

# print(int(np.amax(img)))
# print(int(np.amin(img)))


# img = Image.open('images/sample_640×426.bmp').convert('L')  # convert image to 8-bit grayscale
# WIDTH, HEIGHT = img.size

# data = list(img.getdata()) # convert image data to a list of integers
# # convert that to 2D list (list of lists of integers)
# data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

# # At this point the image's pixels are all in memory and can be accessed
# # individually using data[row][col].

# # For example:
# for row in data:
#     print(' '.join('{:3}'.format(value) for value in row))



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
