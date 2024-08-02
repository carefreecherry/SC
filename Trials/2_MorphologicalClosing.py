'''Morphological Closing'''
''' After basic image enhancement, grayscaling image, applying Gaussian blur and edge detection, 
morphological operations, specifically morphological closing, are used to enhance the detection 
of lines or structures in the image. Connected components analysis (blob analysis) is then 
applied to count the distinct blobs, which correspond to individual sheets. This approach was 
inspired by the abstract of research on machine vision systems for counting corrugated cardboard, 
where the use of morphological operation were mentioned. https://ieeexplore.ieee.org/document/6925889
The output was too small.'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Image at path {image_path} could not be loaded.")
    
    # Apply Gaussian blur to smooth the image
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Perform edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    return edges

def count_sheets(edges):
    # Use morphology operations to extract lines (slitter side)
    kernel = np.ones((5, 50), np.uint8)
    lines = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Use connected components analysis (blob analysis) to count blobs (cut-off side)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(lines, connectivity=8)
    
    # Draw bounding boxes around detected blobs (for visualization)
    output_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    for i in range(1, num_labels):  # Skip background label (0)
        x, y, w, h, area = stats[i]
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Count the number of detected blobs
    sheet_count = num_labels - 1  # Subtract 1 to exclude the background label
    return sheet_count, output_image

def main(image_path):
    # Preprocess the image
    edges = preprocess_image(image_path)
    
    # Count the sheets and get visualization
    sheet_count, output_image = count_sheets(edges)
    
    # Display the result
    print(f'Sheet count: {sheet_count}')
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(edges, cmap='gray')
    plt.title('Edges')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.title(f'Sheet count: {sheet_count}')
    plt.axis('off')
    
    plt.show()

# Example usage
image_path = 'images/3.jpeg'
main(image_path)
