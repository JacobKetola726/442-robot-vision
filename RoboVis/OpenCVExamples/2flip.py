import cv2 as cv

src = cv.imread("japaneseflowers.jpg", 1)
if src is None:
    print("missing image")
else:
    cv.imshow("Original Image", src)
    
    # Flip the image vertically
    dst = cv.flip(src, 0)  # 0 for vertical flip, 1 for horizontal, -1 for both

    cv.imshow("Flipped Image", dst)
    cv.waitKey(0)
    cv.destroyAllWindows()
