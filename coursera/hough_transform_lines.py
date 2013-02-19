import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('point.png',0)
ht = np.zeros(( 500,360),np.uint16)

pts = np.transpose(np.where(img>0))
for (x,y) in pts:
    rhos = []
    for theta in xrange(90):
        rad = np.deg2rad(theta)
        rho = x*np.cos(rad) + y*np.sin(rad)
        rhoadj = np.around(rho)+200
        ht[rhoadj,theta] += 1
        rhos.append(rhoadj)
        
    #plt.plot(rhos)
#plt.imshow(ht,'cool')
#plt.show()
    #break    
v = np.array([ [1,1,1],[1,1,1],[1,1,1]])
htt = cv2.filter2D(ht,2,v)

gotit = np.transpose(np.where(htt > htt.max()-2))
gotit = gotit - np.array([200,0])

for rho,theta in gotit:
    x1,y1 = 0,int((rho)/np.sin(np.deg2rad(theta)))
    x2,y2 = int((rho)/np.cos(np.deg2rad(theta))),0

    cv2.line(img,(y1,x1),(y2,x2),255,1)
plt.imshow(img,cmap = 'cool')
plt.show()

