""" swt - 1 : Doesn't consider the orientation. hopeful """

import numpy as np

import cv2

im = cv2.imread('sofsign.jpg')
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray,50,200)
swt = 255*np.ones(edges.shape,np.uint8)
mask = np.zeros(edges.shape,np.uint8)

dx = cv2.Sobel(edges,cv2.CV_32F,1,0)

dx[np.where(dx<0)] = 0
dx = dx+0.001
dy = cv2.Sobel(edges,cv2.CV_32F,0,1)

angle = np.rad2deg(np.arctan(dy/dx))

##dx = cv2.convertScaleAbs(dx)



rows,cols = edges.shape

for r in xrange(rows):
    for c in xrange(cols):
        if mask.item(r,c)!= 255:
            if edges.item(r,c) == 255:
                points = []
                points.append([r,c])
                for cc in xrange(c+1,cols):
                    if edges.item(r,cc) == 255:
                        points.append([r,cc])
                        break
                    else:
                        points.append([r,cc])

                if len(points)>25:
                    for [rrr,ccc] in points:
                        swt.itemset((rrr,ccc),255)
                        mask.itemset((rrr,ccc),255)
                else:
                    length = len(points)
                    for [rrr,ccc] in points:
                        swt.itemset((rrr,ccc),length)
                        mask.itemset((rrr,ccc),255)
            else:
                mask.itemset((r,c),255)
            
        


cv2.imshow('swt',swt)
cv2.imshow('edges',edges)
cv2.imshow('mask',mask)
ret,swt = cv2.threshold(swt,127,255,1)
cv2.imwrite('sofswt1.png',swt)
cv2.waitKey(0)
cv2.destroyAllWindows()
