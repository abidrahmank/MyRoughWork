""" Rough implementation of Harris Corner Detector and Shi-Tomasi """

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lail.png',0)
img = cv2.equalizeHist(img)
rows,cols = img.shape
#img = cv2.GaussianBlur(img,(5,5),1.4)

# Find Ix, Iy
Ix = cv2.Sobel(img,5,1,0)
Iy = cv2.Sobel(img,5,0,1)

# Find Ix2, Iy2, IxIy
Ix2 = Ix*Ix
Iy2 = Iy*Iy
IxIy = Ix*Iy

# Convolve them with a larger Gaussian Window
##Ix2 = cv2.GaussianBlur(Ix2,(5,5),1.4)
##Iy2 = cv2.GaussianBlur(Iy2,(5,5),1.4)
##IxIy = cv2.GaussianBlur(IxIy,(5,5),1.4)

M = np.dstack((Ix2,IxIy,IxIy,Iy2))

L = np.empty((rows,cols,2))
eig = np.linalg.eigvals

for i in xrange(rows):
    for j in xrange(cols):
        L1,L2 = eig(M[i,j,:].reshape(2,2))
        L.itemset(i,j,0,L1)
        L.itemset(i,j,1,L2)

# For Harris Corners 
R = np.abs(L.prod(axis = 2) - 0.3*np.square(L.sum(axis = 2)))

# For Shi-Tomasi
#R = np.abs(L[:,:,0])

cv2.normalize(R,R,0,1,cv2.NORM_MINMAX)
R = np.where(R>0.9,255,0)
R = np.uint8(R)

img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
contours, hierarchy = cv2.findContours(R,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,-1,255,-1)
##for cnt in contours:
##    cv2.circle(img,tuple(cnt.flatten().tolist()),2,255,-1)


cv2.imshow("edges",R)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
