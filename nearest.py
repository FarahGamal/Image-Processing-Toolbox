import numpy as np
import math

rowSize = 2
colSize = 2
factor = 2
imageArray = [[1,2], [3,4]]
newImageArray = []
def interpolationRound(val):
    if round(val,1) == 0.5:
        val = int(val)
    else:
        val = round(val)
    return val

for i in range(rowSize):
    for j in range(colSize):
        newrow = i/factor
        newcol = j/factor
        newrowImg = interpolationRound(newrow)
        newcolImg = interpolationRound(newcol)
        newImageArray = np.append(newImageArray,imageArray[newrowImg, newcolImg])

print(newImageArray)
# print(int(1.5))
# print(1.5 % 1)
# val = 0.5555
# if round(val,1) == 0.5:
#     val = int(val)
# else:
#     val = round(val)
# print(val)
# final = np.empty((4, 4))
# m = np.array([[1, 2], [3, 4]])
# emp = []
# emp = m[:,0]

# final = np.vstack((emp, emp))

# emp = m[:,1]
# final = np.vstack((emp, emp))

# # for col in m :

# for i in range(len(m)) : 
#     for j in range(len(m[i])) : 
#         print(m[i][j], end=" ")

