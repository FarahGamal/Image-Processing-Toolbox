# Important imports for image processing
import cv2
import numpy as np

# Basic image reading
img = cv2.imread("tssssss.png", 0)
# Shearing factors in X and Y direction
Bx = 1
By = 1
# imread rows and columns
rows = img.shape[0]
cols = img.shape[1]

# Image copies
CopyOf_img1 = np.zeros((rows + cols, cols, 3), np.uint8)
CopyOf_img2 = np.zeros((rows + cols, cols, 3), np.uint8)
CopyOf_img3 = np.zeros((rows, cols + rows, 3), np.uint8)
CopyOf_img4 = np.zeros((rows, cols + rows, 3), np.uint8)


def shearAlgorithm():
    # ShearX algorithm(s)
    for i in range(0, rows):
        for j in range(0, cols):
            n = Bx * i
            k = img[i, j]
            if i >= 0 and i <= rows and j >= 0 and j <= cols:
                CopyOf_img3[i, j + n] = k

    for i in range(0, rows):
        for j in range(0, cols):
            n = Bx * i
            k = img[i, j]
            if i >= 0 and i <= rows and j >= 0 and j <= cols:
                CopyOf_img4[i, j - n + rows] = k

    # # ShearY algorithm(s)
    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         n = By * j
    #         k = img[i, j]

    #         if i >= 0 and i <= rows and j >= 0 and j <= cols:
    #             CopyOf_img1[i + n, j] = k

    # for i in range(0, rows):
    #     for j in range(0, cols):
    #         n = By * j
    #         k = img[i, j]
    #         if i >= 0 and i <= rows and j >= 0 and j <= cols:
    #             CopyOf_img2[i - n + cols, j] = k





    # Show shearX
    cv2.imshow("shearX1", CopyOf_img3)
    cv2.imshow("shearX2", CopyOf_img4)

    # # Writes images to folder and saves them
    # cv2.imwrite('shearY1.PNG', CopyOf_img1)
    # cv2.imwrite('shearY2.PNG', CopyOf_img2)
    # cv2.imwrite('shearX1.PNG', CopyOf_img3)
    # cv2.imwrite('shearX2.PNG', CopyOf_img4)

    # Any key can be pressed to destroy the image and exit out
    cv2.waitKey(0)
    cv2.destroyAllWindows()


shearAlgorithm()