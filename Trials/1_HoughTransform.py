'''Hough Line Transform'''
'''It converts the image to grayscale, applies Gaussian blur, and performs edge detection with Canny.
The Hough Line Transform is then used to identify lines in the image. Uses these lines to calucated number 
of sheet in the stack. But the Number of sheets displayed were too much.'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_lines(image):
    # Convert the uploaded image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Apply Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)

    # Create a copy of the original image to draw lines on
    line_image = image.copy()

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw lines on the image

    # Count the number of detected lines (sheets)
    sheet_count = len(lines) if lines is not None else 0

    # Add text with the sheet count on the image
    text = f"Number of sheets: {sheet_count}"
    cv2.putText(line_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    return sheet_count, line_image

def display_images(original, line_image):
    # Use matplotlib to display images
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))

    plt.subplot(1, 2, 2)
    plt.title('Image with Detected Lines')
    plt.imshow(cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB))

    plt.show()

# Example usage
image_path = 'images/2.jpeg'
image = cv2.imread(image_path)

# Detect lines and get the image with lines drawn and the count
sheet_count, line_image = detect_lines(image)

# Display the results
print(f"Number of sheets detected: {sheet_count}")

# Display the images
display_images(image, line_image)
