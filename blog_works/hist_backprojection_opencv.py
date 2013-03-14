import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('rose_green.png')
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

target = cv2.imread('rose.png')
hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )

cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],1)

disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
dst2 = dst.copy()
ret,thresh = cv2.threshold(dst,50,255,0)
thresh = cv2.merge((dst,dst,dst))
dst2 = cv2.merge((dst,dst,dst))
res = cv2.bitwise_and(target,thresh)

res = np.vstack((target,dst2,res))

cv2.imwrite('res.jpg',res)
