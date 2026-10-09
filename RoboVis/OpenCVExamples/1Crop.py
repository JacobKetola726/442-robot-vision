import cv2 as cv

src = cv.imread("japaneseflowers.jpg", 1)
if src is None:
    print("Missing image")
else:
    cv.imshow("Original Image", src)

    # Get image dimensions
    rows, cols = src.shape[:2]
    print(src.shape)
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    print(src.shape)

    # Define crop size
    crop_size = 150
    start_x = (cols // 2) - (crop_size // 2)
    start_y = (rows // 2) - (crop_size // 2)

    # Crop the image using array slicing
    cropped = src[start_y:start_y + crop_size, start_x:start_x + crop_size]

    cv.imshow("Cropped Image", cropped)
    cv.waitKey(0)
    cv.destroyAllWindows()
