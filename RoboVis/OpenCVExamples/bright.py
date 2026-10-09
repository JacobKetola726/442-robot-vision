import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
cv.namedWindow("Video")

print("start")    
while True:
    status, img = cap.read()
    cv.imshow("Video", img)
    dim = img.shape
    width, height = dim[0], dim[1]
    b = 75 * np.ones((width, height, 3), np.uint8)
    bright = cv.absdiff(img, b)
    #bright = cv.add(img, b)
    cv.imshow("Bright", bright)
    k = cv.waitKey(1)
    if k == 27:
        break
  
cv.destroyAllWindows()
