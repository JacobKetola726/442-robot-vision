import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
cv.namedWindow("Video")

print("start")    
while True:
    status, img = cap.read()
    cv.imshow("Video", img)
    dst = cv.blur(img, (5,5))
    gauss = cv.GaussianBlur(img,(5,5),0)
    med  = cv.medianBlur(img, 5) 
    cv.imshow("blur", dst)
    cv.imshow("Gaussianblur", gauss)
    cv.imshow("filter", med)
    k = cv.waitKey(1)
    if k == 27:
        break

cv.destroyAllWindows()
