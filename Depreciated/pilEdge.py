from PIL import Image
from PIL import ImageFilter

# Open the image
image_path = "recent.jpg"  # Path to the saved image
image = Image.open(image_path)

# Apply Canny edge detection
edges = image.filter(ImageFilter.FIND_EDGES)

# Display the resulting image
edges.show()
