import cv2 as cv

cap = cv.VideoCapture(0)
cv.namedWindow("Video")

print("start")    
while True:
    status, img = cap.read()
    h = img.shape

    
    cv.rectangle(img,(455,5),(500,20),(0,255,255),-1)
    cv.circle(img,(180,0), 50, (0,0,255), 0)
    
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img,'Drawing Demo',(10, h[0]-10 ), font, 1,(255,255,255),1,cv.LINE_AA)
    cv.imshow("Video", img)
    k = cv.waitKey(1)
    if k == 27:
        break

print(img)   
cv.destroyAllWindows()




    
