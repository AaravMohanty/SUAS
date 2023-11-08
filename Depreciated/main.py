import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("recent.jpg", cv2.IMREAD_GRAYSCALE)

img_canny = cv2.Canny(img_gray, threshold1=150, threshold2=250)

plt.figure(1)
plt.subplot(121)
plt.imshow(img_gray, cmap="gray")
plt.title("Image Gray")

plt.subplot(122)
plt.imshow(img_canny, cmap="gray")
plt.title("Canny Image")
plt.show()
