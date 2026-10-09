import cv2 as cv

capture = cv.VideoCapture(0)

if capture == None:
	print ("NULL")
else:
	print ("OK")
	
print ("subscribe done")

cv.namedWindow("original", 1)
cv.namedWindow("Tours", 1)

while(True):
    status, frame = capture.read()
    displayImage = frame.copy()
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY) 
    ret, thresh = cv.threshold(gray,150,255,0) 
	#calculate the contours from binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    with_contours = cv.drawContours(frame,contours,-1,(255,0,0),2)
    for i in contours:
            if i.size > 1050:
                    with_contours = cv.drawContours(frame,contours,-1,(0,0,255),2)

    
    cv.imshow("original", gray)
    cv.imshow("Tours", with_contours)
    if cv.waitKey(10) == 27:
        break
   
cv.destroyAllWindows()
