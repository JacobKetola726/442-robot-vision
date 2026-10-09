import cv2 as cv

global high
global low 
low = high = 0

def mouseCall(evt, x, y, flags, pic):
    #print ("mouse Worked")
    if evt == cv.EVENT_LBUTTONDOWN:
            print (pic.shape, x, y)

def change_Low(value):
    global low
    low = value
    print(low)
    
def change_High(value):
    global high
    high = value
    print(high)

capture = cv.VideoCapture(0)
	
print ("subscribe done")

cv.namedWindow("original", 1)
cv.namedWindow("Canny", 1)
cv.createTrackbar("Low", "Canny", 0, 255,  change_Low)
cv.createTrackbar("High", "Canny", 0, 255, change_High)

while(True):
    status, frame = capture.read()
    displayImage = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    final = cv.Canny(gray, low, high)
    cv.setMouseCallback("original", mouseCall, frame)
    cv.imshow("original", displayImage)
    cv.imshow("Canny", final)
    if cv.waitKey(10) == 27:
        break
   
cv.destroyAllWindows()
