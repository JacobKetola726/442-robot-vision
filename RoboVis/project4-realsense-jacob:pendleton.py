import sys
import numpy as np
import cv2 as cv
import pyrealsense2 as rs
import maestro
 
# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
 
# Camera resolution
FRAME_W = 640
FRAME_H = 480
FPS = 30
 
# Maestro channels (verify these against your Tango's wiring)
PAN_CHANNEL = 3
TILT_CHANNEL = 4
 
# Servo values are in quarter-microseconds (6000 = 1500 us = center)
PAN_CENTER = 6000
TILT_CENTER = 6000
 
# Part 9: safe servo limits (adjust experimentally so nothing binds)
PAN_MIN, PAN_MAX = 4000, 8000
TILT_MIN, TILT_MAX = 4500, 7500
 
# Part 6/7: dead zone in pixels around the image center
DEAD_ZONE_X = 40
DEAD_ZONE_Y = 30
 
# Part 8: small, proportional corrections
# step = error * GAIN, then clamped to MAX_STEP
PAN_GAIN = 0.6     # servo units per pixel of error
TILT_GAIN = 0.6
MAX_STEP = 60      # largest change allowed in a single frame
 
# Direction flags: flip to -1 if the servo moves the wrong way.
# Determine experimentally (Part 7).
PAN_DIRECTION = -1   # object on the left (errorX < 0) -> pan value increases
TILT_DIRECTION = 1   # object above (errorY < 0)       -> tilt value decreases
 
# Part 3: ignore contours smaller than this (pixels^2)
MIN_CONTOUR_AREA = 500
 
# Part 2: HSV limits for orange. Tune for the lab lighting.
# OpenCV HSV ranges: H 0-179, S 0-255, V 0-255
LOWER_HSV = np.array([5, 120, 120])
UPPER_HSV = np.array([20, 255, 255])
 
# Set True to show HSV trackbars for tuning the color limits live
SHOW_TUNING_SLIDERS = True
 
 
# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
 
def clamp(value, low, high):
    return max(low, min(high, value))
 
 
def compute_step(error, dead_zone, gain, direction):
    """Return a small servo correction, or 0 inside the dead zone."""
    if abs(error) <= dead_zone:
        return 0
    step = int(error * gain)
    step = clamp(step, -MAX_STEP, MAX_STEP)
    return step * direction
 
 
def setup_sliders():
    cv.namedWindow("HSV Tuning")
    nothing = lambda x: None
    cv.createTrackbar("H low", "HSV Tuning", int(LOWER_HSV[0]), 179, nothing)
    cv.createTrackbar("H high", "HSV Tuning", int(UPPER_HSV[0]), 179, nothing)
    cv.createTrackbar("S low", "HSV Tuning", int(LOWER_HSV[1]), 255, nothing)
    cv.createTrackbar("S high", "HSV Tuning", int(UPPER_HSV[1]), 255, nothing)
    cv.createTrackbar("V low", "HSV Tuning", int(LOWER_HSV[2]), 255, nothing)
    cv.createTrackbar("V high", "HSV Tuning", int(UPPER_HSV[2]), 255, nothing)
 
 
def read_sliders():
    lo = np.array([cv.getTrackbarPos("H low", "HSV Tuning"),
                   cv.getTrackbarPos("S low", "HSV Tuning"),
                   cv.getTrackbarPos("V low", "HSV Tuning")])
    hi = np.array([cv.getTrackbarPos("H high", "HSV Tuning"),
                   cv.getTrackbarPos("S high", "HSV Tuning"),
                   cv.getTrackbarPos("V high", "HSV Tuning")])
    return lo, hi
 
 
# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
 
def main():
    # --- Servo setup ---
    servo = maestro.Controller()
    pan_pos = PAN_CENTER
    tilt_pos = TILT_CENTER
 
    # Speed/acceleration limits make the motion smoother (0 = unlimited)
    servo.setSpeed(PAN_CHANNEL, 40)
    servo.setSpeed(TILT_CHANNEL, 40)
    servo.setAccel(PAN_CHANNEL, 10)
    servo.setAccel(TILT_CHANNEL, 10)
 
    servo.setTarget(PAN_CHANNEL, pan_pos)
    servo.setTarget(TILT_CHANNEL, tilt_pos)
 
    # --- Part 1: RealSense pipeline, color stream only ---
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, FRAME_W, FRAME_H, rs.format.bgr8, FPS)
 
    try:
        pipeline.start(config)
    except RuntimeError as e:
        print("Could not start RealSense camera:", e)
        servo.close()
        sys.exit(1)
 
    center_x = FRAME_W // 2
    center_y = FRAME_H // 2
    kernel = np.ones((5, 5), np.uint8)
 
    if SHOW_TUNING_SLIDERS:
        setup_sliders()
 
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
 
            # Convert RealSense frame -> NumPy array OpenCV can use
            image = np.asanyarray(color_frame.get_data())
 
            # --- Part 2: HSV threshold to a binary mask ---
            hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            if SHOW_TUNING_SLIDERS:
                lower, upper = read_sliders()
            else:
                lower, upper = LOWER_HSV, UPPER_HSV
            mask = cv.inRange(hsv, lower, upper)
 
            # Clean up noise: remove specks, fill small holes
            mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
            mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
 
            # --- Part 3: find the largest valid contour ---
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL,
                                          cv.CHAIN_APPROX_SIMPLE)
            target = None
            if contours:
                largest = max(contours, key=cv.contourArea)
                if cv.contourArea(largest) >= MIN_CONTOUR_AREA:
                    target = largest
 
            # Draw image center and dead zone
            cv.drawMarker(image, (center_x, center_y), (255, 0, 0),
                          cv.MARKER_CROSS, 20, 2)
            cv.rectangle(image,
                         (center_x - DEAD_ZONE_X, center_y - DEAD_ZONE_Y),
                         (center_x + DEAD_ZONE_X, center_y + DEAD_ZONE_Y),
                         (255, 0, 0), 1)
 
            if target is not None:
                # --- Part 4: center of object using moments ---
                M = cv.moments(target)
                if M["m00"] != 0:
                    obj_x = int(M["m10"] / M["m00"])
                    obj_y = int(M["m01"] / M["m00"])
 
                    cv.drawContours(image, [target], -1, (0, 255, 0), 2)
                    cv.circle(image, (obj_x, obj_y), 8, (0, 0, 255), -1)
 
                    # --- Part 5: tracking error ---
                    # errorX < 0 -> object is left; errorY < 0 -> object is above
                    error_x = obj_x - center_x
                    error_y = obj_y - center_y
 
                    # --- Parts 6-8: small corrections outside the dead zone ---
                    pan_step = compute_step(error_x, DEAD_ZONE_X,
                                            PAN_GAIN, PAN_DIRECTION)
                    tilt_step = compute_step(error_y, DEAD_ZONE_Y,
                                             TILT_GAIN, TILT_DIRECTION)
 
                    # --- Part 9: enforce servo limits ---
                    new_pan = clamp(pan_pos + pan_step, PAN_MIN, PAN_MAX)
                    new_tilt = clamp(tilt_pos + tilt_step, TILT_MIN, TILT_MAX)
 
                    if new_pan != pan_pos:
                        pan_pos = new_pan
                        servo.setTarget(PAN_CHANNEL, pan_pos)
                    if new_tilt != tilt_pos:
                        tilt_pos = new_tilt
                        servo.setTarget(TILT_CHANNEL, tilt_pos)
 
                    status = f"errX={error_x:+4d} errY={error_y:+4d}  pan={pan_pos} tilt={tilt_pos}"
                    cv.putText(image, status, (10, 25), cv.FONT_HERSHEY_SIMPLEX,
                               0.6, (0, 255, 255), 2)
            else:
                cv.putText(image, "No target", (10, 25), cv.FONT_HERSHEY_SIMPLEX,
                           0.6, (0, 0, 255), 2)
 
            cv.imshow("RealSense Tracking", image)
            cv.imshow("Mask", mask)
 
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
 
    finally:
        # Return head to center and clean up
        servo.setTarget(PAN_CHANNEL, PAN_CENTER)
        servo.setTarget(TILT_CHANNEL, TILT_CENTER)
        pipeline.stop()
        servo.close()
        cv.destroyAllWindows()
 
 
if __name__ == "__main__":
    main()
