'''CONTOUR DETECTION'''
'''This approach detects the number of sheets in an image by first converting it to grayscale 
and applying Gaussian blur to reduce noise. Canny edge detection is then used to identify edges, 
and contours are extracted to locate the sheets. The contours are drawn on a copy of the original image, 
and the total count of detected sheets is overlayed as text on the annotated image.  The output was too big.'''

import cv2
import numpy as np  
import matplotlib.pyplot as plt

def count_sheets(image):
    # Convert the uploaded image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    contour_image = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 2)

    # Count the number of contours
    sheet_count = len(contours)
    
    # Add text with the sheet count on the image
    text = f"Number of sheets: {sheet_count}"
    cv2.putText(contour_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    return sheet_count, contour_image

def display_images(original, contour_image):
    # Use matplotlib to display images
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))

    plt.subplot(1, 2, 2)
    plt.title('Annotated Image with Contours')
    plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))

    plt.show()

# Example usage
image_path = 'images/2.jpeg'
image = cv2.imread(image_path)

# Count the sheets and get the contour image
sheet_count, contour_image = count_sheets(image)

# Display the images
display_images(image, contour_image)
