import cv2 as cv

cap = cv.VideoCapture(2)

print("start")    
while True:
    success, img = cap.read()

    if not success or img is None:
        print("Failed to grab frame. Exiting or retrying")
        break

    cv.imshow("Video", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
    
    
