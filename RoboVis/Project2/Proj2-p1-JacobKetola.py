import cv2 as cv
import numpy as np

Win_orig = "Original"
Win_HSV = "HSV"
Win_mask = "Mask"
Win_control = "Controls"

SAMPLE_RADIUS = 5 #Sample an 11x11 patch around the click, not just one pixel
Padding = (10, 40, 40) # Extra margin added to the sampled H, S, V range
hsv_frame = None

def nothing(_):
    
    pass

def on_mouse(event, x, y, flags, param):
    
    if event != cv.EVENT_LBUTTONDOWN  or hsv_frame is None:
        return

    h, w = hsv_frame.shape[:2]

    x0, x1 = max(0, x - SAMPLE_RADIUS), min(w, x + SAMPLE_RADIUS + 1)
    y0, y1 = max(0, y - SAMPLE_RADIUS), min(h, y + SAMPLE_RADIUS + 1)

    patch = hsv_frame[y0:y1, x0:x1].reshape(-1, 3)
    mins = patch.min(axis=0)
    maxs = patch.max(axis=0)
    median = np.median(patch, axis=0).astype(int)

    print(f"\nClicked ({x}, {y}) - sampled {len(patch)} pixels")
    print(f" Center pixel HSV: {hsv_frame[y, x]}")
    print(f" Min HSV: {mins}")
    print(f" Median HSV: {median}")
    print(f" Max HSV: {maxs}")

    limits = (179, 255, 255)
    names = ("H", "S", "V")
    for i in range(3):
        lo = max(0, int(mins[i]) - Padding[i])
        hi = min(limits[i], int(maxs[i]) + Padding[i])
        cv.setTrackbarPos(f"{names[i]} min", Win_control, lo)
        cv.setTrackbarPos(f"{names[i]} max", Win_control, hi)

def create_controls():
    cv.namedWindow(Win_control)
    cv.resizeWindow(Win_control, 200, 350)
    cv.createTrackbar("H min", Win_control, 0, 179, nothing)
    cv.createTrackbar("H max", Win_control, 179, 179, nothing)
    cv.createTrackbar("S min", Win_control, 0, 255, nothing)
    cv.createTrackbar("S max", Win_control, 255, 255, nothing)
    cv.createTrackbar("V min", Win_control, 0, 255, nothing)
    cv.createTrackbar("V max", Win_control, 255, 255, nothing)
    cv.createTrackbar("Erode iter", Win_control, 2, 10, nothing)
    cv.createTrackbar("Dilate iter", Win_control, 4, 10, nothing)

def read_controls():
    g = lambda name: cv.getTrackbarPos(name, Win_control)
    lower = np.array([g("H min"), g("S min"), g("V min")], dtype=np.uint8)
    upper = np.array([g("H max"), g("S max"), g("V max")], dtype=np.uint8)
    return lower, upper, g("Erode iter"), g("Dilate iter")

def main():
    global hsv_frame

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    cv.namedWindow(Win_orig)
    cv.namedWindow(Win_HSV)
    cv.namedWindow(Win_mask)
    create_controls()
    cv.setMouseCallback(Win_HSV, on_mouse)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        blurred = cv.GaussianBlur(frame, (5, 5), 0)

        hsv_frame = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        lower, upper, erode_iter, dilate_iter = read_controls()

        mask = cv.inRange(hsv_frame, lower, upper)

        mask = cv.erode(mask, kernel, iterations=erode_iter)
        mask = cv.dilate(mask, kernel, iterations=dilate_iter)

        
        display = frame.copy()
        contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

        if contours:
            biggest = max(contours, key=cv.contourArea)
            if cv.contourArea(biggest) > 300:
                M = cv.moments(biggest)
                cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
                x, y, w, h = cv.boundingRect(biggest)
                cv.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv.circle(display, (cx, cy), 5, (0, 0, 255), -1)

        cv.imshow(Win_orig, display)
        cv.imshow(Win_HSV, hsv_frame)
        cv.imshow(Win_mask, mask)

        key = cv.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
        
    




    

    
