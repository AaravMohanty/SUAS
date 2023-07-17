import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

def kmeans_color_segmentation(image_path, num_clusters=2, tolerance=30):
    image = Image.open('recent.jpg')
    image = image.convert("RGB")
    
    # Reshape the image to a 2D array of pixels
    pixels = np.array(image).reshape(-1, 3)
    
    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)
    
    # Get the labels and cluster centers
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    
    # Determine the color of interest (cluster with the largest number of pixels)
    unique_labels, counts = np.unique(labels, return_counts=True)
    color_of_interest = centers[np.argmax(counts)]
    
    # Create a mask based on the color of interest and tolerance
    mask = np.linalg.norm(np.array(image) - color_of_interest, axis=2) <= tolerance
    
    # Apply the mask to the original image
    segmented_image = Image.fromarray(np.where(mask[:, :, np.newaxis], np.array(image), 0).astype(np.uint8))
    
    return segmented_image

image_path = 'recent.jpg'
segmented_image = kmeans_color_segmentation(image_path, num_clusters=2, tolerance=30)

# Display
segmented_image.show()
