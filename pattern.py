import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image = Image.open("patterned image.jpeg").convert("L")
imag_arr = np.asarray(image)

img_height = imag_arr.shape[0]
img_width = imag_arr.shape[1]
filter_arr = np.full((img_height, img_width), 1)
filter_arr[475:495,375:395] = 0
filter_arr[555:575,375:395] = 0
filter_arr[475:495,325: 340] = 0
filter_arr[555:575,325: 340] = 0

filter_arr[435:455,375:395] = 0
filter_arr[435:455,325: 335] = 0
filter_arr[605:625,325: 340] = 0
filter_arr[605:625,380:395] = 0

ft_image_np = np.fft.fft2(imag_arr)
fshift = np.fft.fftshift( ft_image_np)
real_component =  fshift.real
imaginary_component =  fshift.imag

magnitude = np.sqrt(( real_component ** 2) + ( imaginary_component ** 2))
log_magnitude = np.log( magnitude + 1)

filtered = fshift * filter_arr
restored_img = ((np.fft.ifft2(np.fft.ifftshift(filtered))))
real_component = restored_img.real
imaginary_component = restored_img.imag
restored_img_mag = np.sqrt((real_component ** 2) + (imaginary_component ** 2))
trial = log_magnitude * filter_arr

plt.matshow(trial, cmap='gray') # trial, restored_img
plt.matshow(log_magnitude, cmap='gray')
plt.matshow(restored_img_mag, cmap='gray')

plt.show()
