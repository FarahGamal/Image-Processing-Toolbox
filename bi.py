# # import numpy as np

# # def bilinear_interpolate(im, x, y):
# #     x = np.asarray(x)
# #     y = np.asarray(y)

# #     x0 = np.floor(x).astype(int)
# #     x1 = x0 + 1
# #     y0 = np.floor(y).astype(int)
# #     y1 = y0 + 1

# #     x0 = np.clip(x0, 0, im.shape[1]-1)
# #     x1 = np.clip(x1, 0, im.shape[1]-1)
# #     y0 = np.clip(y0, 0, im.shape[0]-1)
# #     y1 = np.clip(y1, 0, im.shape[0]-1)

# #     Ia = im[ y0, x0 ]
# #     Ib = im[ y1, x0 ]
# #     Ic = im[ y0, x1 ]
# #     Id = im[ y1, x1 ]

# #     wa = (x1-x) * (y1-y)
# #     wb = (x1-x) * (y-y0)
# #     wc = (x-x0) * (y1-y)
# #     wd = (x-x0) * (y-y0)

# #     return wa*Ia + wb*Ib + wc*Ic + wd*Id

# import numpy as np
# array_in = [[1, 2 , 3 , 4], [1, 2 , 3 , 4], [1, 2 , 3 , 4], [1, 2 , 3 , 4]]
# width_in = 4
# height_in = 4
# def interpolate_bilinear(array_in, width_in, height_in, array_out, width_out, height_out):
#     for i in range(height_out):
#         for j in range(width_out):
#             # Relative coordinates of the pixel in output space
#             x_out = j / width_out
#             y_out = i / height_out

#             # Corresponding absolute coordinates of the pixel in input space
#             x_in = (x_out * width_in)
#             y_in = (y_out * height_in)

#             # Nearest neighbours coordinates in input space
#             x_prev = int(np.floor(x_in))
#             x_next = x_prev + 1
#             y_prev = int(np.floor(y_in))
#             y_next = y_prev + 1

#             # Sanitize bounds - no need to check for < 0
#             x_prev = min(x_prev, width_in - 1)
#             x_next = min(x_next, width_in - 1)
#             y_prev = min(y_prev, height_in - 1)
#             y_next = min(y_next, height_in - 1)
            
#             # Distances between neighbour nodes in input space
#             Dy_next = y_next - y_in
#             Dy_prev = 1. - Dy_next # because next - prev = 1
#             Dx_next = x_next - x_in
#             Dx_prev = 1. - Dx_next # because next - prev = 1
            
#             # Interpolate over 3 RGB layers
#             for c in range(3):
#                 array_out[i][j][c] = Dy_prev * (array_in[y_next][x_prev][c] * Dx_next + array_in[y_next][x_next][c] * Dx_prev) + Dy_next * (array_in[y_prev][x_prev][c] * Dx_next + array_in[y_prev][x_next][c] * Dx_prev)
                
#     return array_out
# array_out = []
# interpolate_bilinear(array_in, width_in, height_in, array_out, 8, 8)
import operator
x=1
n=2

# NearestTimestep = getattr(x, max)
print(min(5, 50-1))
# print(NearestTimestep)
# print(operator.lt(x, n))