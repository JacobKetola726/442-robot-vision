import cv2
import numpy as np

WIN_CTRL = "Controls"

def nothing(_):
    pass

def create_controls():
    cv2.namedWindow(WIN_CTRL)
    cv2.resizeWindow(WIN_CTRL, 400, 300)
    cv2.createTrackbar("Alpha x1000", WIN_CTRL, 20, 200, nothing)
    cv2.createTrackbar("Brightness", WIN_CTRL, 20, 100, nothing)
    cv2.createTrackbar("Threshold 1", WIN_CTRL, 25, 255, nothing)
    cv2.createTrackbar("Threshold 2", WIN_CTRL, 40, 255, nothing)
    cv2.createTrackbar("Min area", WIN_CTRL, 1500, 20000, nothing)

def read_controls():
    g = lambda name: cv2.getTrackbarPos(name, WIN_CTRL)
    alpha = max(g("Alpha x1000"), 1) / 1000.0
    return alpha, g("Brightness"), g("Threshold 1"), g("Threshold 2"), g("Min area")

def preprocess(frame, brightness):

    bright = cv2.convertScaleAbs(frame, alpha=1.0, beta=brightness)
    return cv2.GaussianBlur(bright, (21, 21), 0)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    create_controls()
    
    avg = None
 
    while True:
        ok, frame = cap.read()
        if not ok:
            break
 
        alpha, brightness, t1, t2, min_area = read_controls()
        processed = preprocess(frame, brightness)
 
        
        if avg is None:
            avg = processed.astype(np.float32)   # same as np.float32(processed)
            continue
 
        background = cv2.convertScaleAbs(avg)
 
        diff = cv2.absdiff(processed, background)
 
        cv2.accumulateWeighted(processed, avg, alpha)
 
        # ---- Grayscale ----
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
 
        # ---- Threshold -> blur -> threshold ----
        _, binary = cv2.threshold(gray_diff, t1, 255, cv2.THRESH_BINARY)
        binary = cv2.GaussianBlur(binary, (15, 15), 0)
        _, binary = cv2.threshold(binary, t2, 255, cv2.THRESH_BINARY)
        binary = cv2.dilate(binary, None, iterations=2)
 
        contours = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]
 
        contour_vis = np.zeros_like(frame)
        cv2.drawContours(contour_vis, contours, -1, (128, 128, 128), 1)
 
        output = frame.copy()
        significant = 0
        for c in contours:
            # Reject insignificant contours: noise, flicker, single pixels,
            # and small shadow fragments all produce tiny areas.
            if cv2.contourArea(c) < min_area:
                continue
            significant += 1
 
            cv2.drawContours(contour_vis, [c], -1, (0, 255, 0), 2)
 
            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
            # Center using image moments (centroid of the contour area)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx, cy = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
            else:
                cx, cy = x + w // 2, y + h // 2
            cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(output, f"({cx},{cy})", (cx + 8, cy - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
 
        cv2.putText(output, f"Moving regions: {significant}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
 
        cv2.imshow("Motion", output)
        cv2.imshow("Background", background)
        cv2.imshow("Difference", gray_diff)
        cv2.imshow("Binary", binary)
        cv2.imshow("Contours", contour_vis)
 
        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        if key == ord("r"):
            avg = None  # rebuild the background from the next frame
 
    cap.release()
    cv2.destroyAllWindows()
 
 
if __name__ == "__main__":
    main()
 
