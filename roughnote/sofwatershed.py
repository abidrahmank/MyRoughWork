'''simple watershed example '''

import cv2
import numpy as np

img = cv2.imread('sofwatershed.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite('sofwsthresh.png',thresh)
fg = cv2.erode(thresh,None,iterations = 2)

bgt = cv2.dilate(thresh,None,iterations = 2)

ret,bg = cv2.threshold(bgt,1,128,1)

marker = cv2.add(fg,bg)

marker32 = np.int32(marker)

cv2.watershed(img,marker32)
m = cv2.convertScaleAbs(marker32)

ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
thresh = cv2.bitwise_and(img,img,mask = thresh)

cv2.imshow('win',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

