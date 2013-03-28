""" Rough implementation of Harris Corner Detector and Shi-Tomasi """

import cv2,time
import numpy as np
from matplotlib import pyplot as plt

imgc = cv2.imread('sof2.png')
img = cv2.imread('sof2.png',0)


edges = cv2.Canny(img,50,150)

contours,hierarchy = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

cnt = contours[0].reshape((-1,2))
rows,cols = cnt.shape

first = np.array([0,0])

change = np.diff(cnt,axis = 0)
norm = change[:,0]*9 + change[:,1] + 10

palette = np.arange(21)
palette[[19,18,9,0,1,2,11,20]] = range(8)

path = palette[norm]
path = np.convolve(path,np.ones(5))

    

cv2.imshow("edges",edges)
cv2.imshow('img',imgc)
cv2.waitKey(0)
cv2.destroyAllWindows()
