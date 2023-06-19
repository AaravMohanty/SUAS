import cv2
import matplotlib.pyplot as plt

# Create a VideoCapture object to capture video from the default camera
cap = cv2.VideoCapture(0)

while True:
    # Read the current frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to the grayscale frame
    edges = cv2.Canny(frame_gray, threshold1=150, threshold2=250)

    # Display the original frame and the Canny edges
    plt.figure(1)
    plt.subplot(121)
    plt.imshow(frame_gray, cmap="gray")
    plt.title("Grayscale Image")

    plt.subplot(122)
    plt.imshow(edges, cmap="gray")
    plt.title("Canny Edges")
    plt.pause(0.001)
    plt.clf()

    # Check for the 'q' key press to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the VideoCapture object and close the display window
cap.release()
cv2.destroyAllWindows()
plt.close()
