import numpy as np
from PIL import Image

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


# array[:,:100] = [255, 128, 0] #Orange left side
# array[:,100:] = [0, 0, 0]   #Blue right side

img = Image.fromarray(array)
img.show()
img.save('testrgb.png')