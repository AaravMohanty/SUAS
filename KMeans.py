import numpy as np
from sklearn.cluster import KMeans
from PIL import Image


def kmeans_color_segmentation(image_path, num_clusters=2, tolerance=255, resize_factor=0.05):
    image = Image.open(image_path)
    image = image.convert("RGB")

    # Resize the image
    new_width = int(image.width * resize_factor)    
    new_height = int(image.height * resize_factor)
    resized_image = image.resize((new_width, new_height))

    # Reshape the resized image to a 2D array of pixels
    pixels = np.array(resized_image).reshape(-1, 3)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)

    # Get the labels and cluster centers
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Determine the color of interest (cluster with the largest number of pixels)
    unique_labels, counts = np.unique(labels, return_counts=True)
    background_color = centers[np.argmax(counts)]

    # Create a mask based on the background color and tolerance
    mask = np.linalg.norm(np.array(resized_image) - background_color, axis=2) > tolerance

    # Apply the mask to the resized image
    segmented_image = Image.fromarray(np.where(mask[:, :, np.newaxis], np.array(resized_image), 0).astype(np.uint8))

    # Resize the segmented image back to the original size
    segmented_image = segmented_image.resize((image.width, image.height))

    return segmented_image


image_path = 'recent.jpg'
segmented_image = kmeans_color_segmentation(image_path, num_clusters=2, tolerance=255, resize_factor=0.05)

# Display
segmented_image.show()
