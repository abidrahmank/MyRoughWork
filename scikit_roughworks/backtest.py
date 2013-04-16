import numpy as np
import cv2
from backproject import histogram_backproject as bp
from matplotlib import pyplot as plt
from skimage import data

img1 = cv2.imread('rose.png',0)
img2 = cv2.imread('rose_red.png',0)

b = bp(img1,img2)

img1 = cv2.imread('rose.png')
img2 = cv2.imread('rose_red.png')


bc = bp(img1,img2)


ret,thresh = cv2.threshold(bc,0.1*255,255,0)

res = cv2.bitwise_and(img1,img1,mask = thresh)
#cv2.imshow('img',thresh)
cv2.imshow('img2',bc)
cv2.imshow('res',res)
thresh = cv2.cvtColor(bc,cv2.COLOR_GRAY2BGR)
x = np.vstack((img1,thresh,res))
cv2.imwrite('img.png',x)

cv2.waitKey(0)
cv2.destroyAllWindows()

