from PIL import Image
import cv2 as cv

# Open the image
image_path = "recent.jpg"
image = Image.open(image_path)

# Display the image using OpenCV
cv_image = cv.cvtColor(cv.imread(image_path), cv.COLOR_BGR2RGB)
cv.namedWindow("Image")
cv.imshow("Image", cv_image)
cv.waitKey(0)
cv.destroyAllWindows()

# Ask the user to draw a bounding box interactively
print("Draw a rectangle to specify the region of interest.")
print("Press 'Enter' to confirm the selection.")
imagedraw = cv.selectROI(cv_image, False)

# Crop the image
cropped_image = image.crop((imagedraw[0], imagedraw[1], imagedraw[0]+imagedraw[2], imagedraw[1]+imagedraw[3]))

# Save the cropped image
cropped_image.save("cropped.jpg")
