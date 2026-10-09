import cv2 as cv
import numpy as np

def mouseCall(evt, x, y, flags, pic):
    #print ("mouse Worked")
    if evt == cv.EVENT_LBUTTONDOWN:
            print (pic.shape, x, y)
            print(pic[y][x])

cap = cv.VideoCapture(0)
cv.namedWindow("Video")

print("start")    
while True:
    status, img = cap.read()
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    cv.setMouseCallback("Video", mouseCall, hsv)
    minArr = np.array([1, 99, 250])
    maxArr = np.array([7, 106, 260])
     
    #using inrage to create 
    bw = cv.inRange(hsv, minArr, maxArr)
     
    
    
    k = cv.waitKey(1)
    if k == 27:
        break
    cv.imshow("Video", hsv)
    cv.imshow("Tracker", bw)
cv.destroyAllWindows()
