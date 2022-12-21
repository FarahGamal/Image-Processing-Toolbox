# CT phantom
# from phantominator import shepp_logan
# from PIL import Image
# import matplotlib.pyplot as plt
# import numpy as np
# ph = shepp_logan(128)
# image = Image.fromarray(np.uint8(ph))
# print(ph)
# image.save("schepp-logan.jpg")
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

from skimage.data import shepp_logan_phantom
from skimage.transform import radon, rescale

image = shepp_logan_phantom()
# for i in range(len(image)):
#     for j in range(len(image[0])):
#         if image[i, j] < 0:
#             image[i, j] = 0
#         elif image[i, j] > 255:
#             image[i, j] = 255 
# print(np.max(image))
image = rescale(image, scale=0.65, mode='reflect', channel_axis=None)

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))

# ax1.set_title("Original")
plt.imshow(image, cmap=plt.cm.Greys_r)

# theta = np.linspace(0., 180., max(image.shape), endpoint=False)
# sinogram = radon(image, theta=theta)
# dx, dy = 0.5 * 180.0 / max(image.shape), 0.5 / sinogram.shape[0]
# ax2.set_title("Radon transform\n(Sinogram)")
# ax2.set_xlabel("Projection angle (deg)")
# ax2.set_ylabel("Projection position (pixels)")
# ax2.imshow(sinogram, cmap=plt.cm.Greys_r,
#            extent=(-dx, 180.0 + dx, -dy, sinogram.shape[0] + dy),
#            aspect='auto')

# fig.tight_layout()
plt.show()

