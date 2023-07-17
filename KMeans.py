import cv2
import numpy as np
from sklearn.cluster import KMeans


def kmeans_color_segmentation(image_path, num_clusters=2, tolerance=120):
    # Load the image
    image = cv2.imread("recent.jpg")

    # Reshape the image to a 2D array of pixels
    pixels = image.reshape(-1, 3)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(pixels)

    # Get the labels and cluster centers
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_

    # Determine the color of interest (cluster center with the highest count)
    cluster_avg_intensities = np.mean(centers, axis=1)
    color_of_interest = centers[np.argmax(cluster_avg_intensities)]

    # Create a mask based on the color of interest and tolerance
    mask = np.linalg.norm(image - color_of_interest, axis=2) <= tolerance

    # Apply the mask to the original image
    result = np.where(mask[:, :, np.newaxis], image, 0)

    return result


# Test the code
image_path = 'recent.jpg'
segmented_image = kmeans_color_segmentation(image_path, num_clusters=2, tolerance=120)

# Display the segmented image
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
