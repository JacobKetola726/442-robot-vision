import cv2 as cv

src = cv.imread("japaneseflowers.jpg", 1)
#src = cv.imread("me.jpg", 1)
if src is None:
    print("missing image")
else:
    
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imshow("windowM", src)
    equ = cv.equalizeHist(src)    
    cv.imshow("windowMy", equ)
                

#equ = cv.equalizeHist(img)
#res = np.hstack((img,equ)) #stacking images side-by-side
#cv.imwrite('res.png',res)            
                
