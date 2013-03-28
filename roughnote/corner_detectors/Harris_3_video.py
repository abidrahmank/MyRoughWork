""" Rough implementation of Harris Corner Detector and Shi-Tomasi """

import cv2,time
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(True):
    
    _,img= cap.read()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #img = cv2.equalizeHist(f)
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
    a = Ix2 = cv2.GaussianBlur(Ix2,(5,5),1)
    d = Iy2 = cv2.GaussianBlur(Iy2,(5,5),1)
    b = c = IxIy = cv2.GaussianBlur(IxIy,(5,5),1)

    Trace = a+d
    Det = a*d - np.square(b)

    #R = np.abs(Trace-0.04*np.square(Det))
    R = Det/(Trace+1)

    cv2.normalize(R,R,0,1,cv2.NORM_MINMAX)
    R = np.where(R>0.5,255,0)
    R = np.uint8(R)

    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    contours, hierarchy = cv2.findContours(R,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        m = cv2.moments(cnt)
        if m['m00'] != 0:
            x = int(m['m10']/m['m00'])
            y = int(m['m01']/m['m00'])
        else:
            x,y = cnt.flatten()[:2]
        cv2.circle(img,(x,y),2,255,-1)

    cv2.imshow("edges",R)
    cv2.imshow('img',img)
    if cv2.waitKey(20) == 27:
        break
    
cv2.destroyAllWindows()
cap.release()
