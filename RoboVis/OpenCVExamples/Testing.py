import cv2

# Initialize the camera (0 is usually the built-in FaceTime HD camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera. Check macOS privacy permissions.")
    exit()

print("Camera active. Press 'q' on your keyboard to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame reading failed, break the loop
    if not ret:
        print("Error: Couldn't receive frame. Exiting...")
        break

    # Display the frame in a window named 'Camera Feed'
    cv2.imshow('Camera Feed', frame)

    # Wait for 1 millisecond; exit loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
