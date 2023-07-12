from PIL import Image
import cv2 as cv

# Open the image
image_path = "recent.jpg"
image = Image.open(image_path)

#using selectROI() function to draw the bounding box around the required objects
imagedraw = cv.selectROI(image)
#cropping the area of the image within the bounding box using imCrop() function
croppedimage = image[int(imagedraw[1]):int(imagedraw[1]+imagedraw[3]), int(imagedraw[0]):int(imagedraw[0]+imagedraw[2])]

# Save the cropped image
croppedimage.save("cropped.jpg")
