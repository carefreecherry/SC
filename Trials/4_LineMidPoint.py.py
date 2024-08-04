'''This approach improves sheet counting accuracy by preprocessing the image with rotation, grayscale conversion, 
and contrast stretching. It uses Canny edge detection and Hough Line Transform to identify lines and compute their 
midpoints. By analyzing the distances between midpoints and removing outliers based on mean squared error, it refines 
the count. The final image is visualized with circles at detected midpoints, and the total sheet count is displayed 
and printed. This method offers better results than simpler techniques but may still have room for improvement. This
approach works only for Horizontal sheets.'''

import cv2
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp

# Define SymPy variables
x, b = sp.symbols('x b')

def rotate_image(image, angle):
    """ Rotate the image by the specified angle. """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Compute the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Perform the rotation
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)
    
    return rotated

def contrast_stretching(img, low_in, high_in, low_out, high_out):
    """ Apply contrast stretching to an image. """
    img = np.float32(img)
    stretched = np.clip((img - low_in) * ((high_out - low_out) / (high_in - low_in)) + low_out, 0, 255)
    return np.uint8(stretched)

# Read the input image
img0 = cv2.imread('images/3.jpeg')

# Rotate the image by 90 degrees
img0 = rotate_image(img0, 90)

# Convert the image to grayscale
gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

# Apply contrast stretching
low_in, high_in = np.min(gray), np.max(gray)  # Input range
low_out, high_out = 0, 255  # Output range
gray = contrast_stretching(gray, low_in, high_in, low_out, high_out)

# Apply Gaussian blur multiple times to reduce noise
for _ in range(5):
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

# Apply Canny edge detection
gray = cv2.Canny(gray, 100, 200)

# Display the processed image
plt.imshow(gray, cmap='gray')
plt.title('Processed Image')
plt.show()

# Create an empty image to draw lines on
img = np.zeros(gray.shape)

# Use Hough Line Transform to detect lines
lines = cv2.HoughLinesP(gray.copy(), 1, np.pi/180, 100, minLineLength=150, maxLineGap=25)
mid_xs = []

# Loop through the detected lines
for x1, y1, x2, y2 in lines.reshape(-1, 4):
    if x2 == x1:
        # Skip vertical lines
        continue
    
    slope = (y2 - y1) / (x2 - x1)  # Calculate the slope
    intercept = sp.Symbol('b')  # Define the intercept symbol
    eq = sp.Eq(slope * x1 + intercept, y1)  # Equation for y-intercept
    intercept_solution = sp.solve(eq, intercept)

    if not intercept_solution:
        # If no intercept is found, skip this line
        print(f"Skipping line: vertical or no intercept found.")
        continue
    
    intercept_value = intercept_solution[0]
    mid_x_eq = slope * x + intercept_value - 600  # Define the equation for midpoint
    mid_x_solution = sp.solve(mid_x_eq, x)

    if not mid_x_solution:
        print(f"No midpoint found for line ({x1}, {y1}) to ({x2}, {y2})")
        continue

    mid_x = float(mid_x_solution[0])
    mid_xs.append(mid_x)
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)  # Draw the line on the image

# Sort the midpoint x-coordinates
mid_xs = np.sort(np.array(mid_xs))

# Calculate the distances between consecutive midpoints
distances = mid_xs[1:] - mid_xs[:-1]
median = np.median(distances)

# Function to calculate mean squared error
def calc_mean_sq_error(arr):
    if len(arr) < 2:
        return float('inf')  # Return a large number if not enough elements
    distances = arr[1:] - arr[:-1]
    return np.mean((distances - median) ** 2)

# Function to decide which points to remove based on mean squared error
def decide_what_to_remove(indices):
    to_delete = []
    for i in indices:
        if i-1 < 0 or i+2 >= len(mid_xs):
            continue  # Skip if indices are out of bounds
        
        arr = mid_xs[i - 1:i + 3]
        if len(arr) < 3:
            continue  # Skip if not enough elements to remove
        
        mse1 = calc_mean_sq_error(np.delete(arr, 1))
        mse2 = calc_mean_sq_error(np.delete(arr, 2))
        to_delete.append(i if mse1 < mse2 else i + 1)
    
    return to_delete

# Find problematic distances and determine which points to delete
problematic_distances = np.where(np.abs(distances - median) > 15)[0]
to_delete = decide_what_to_remove(problematic_distances)
mid_xs = np.delete(mid_xs, to_delete, axis=0)

# Read the original image again to draw the final results
img = cv2.imread('images/1.jpeg')

# Rotate the image back to its original orientation if needed
img = rotate_image(img, -90)  # Rotate back by -90 degrees

# Draw circles on the final midpoint x-coordinates
for x in mid_xs:
    cv2.circle(img, (int(x), 600), 5, (0, 255, 0), 2)

# Display the final image with detected midpoints
plt.imshow(img, cmap='gray')
plt.title(f"Total Sheets: {len(mid_xs)}")
plt.show()

# Print the total number of sheets
print(f"Total number of sheets: {len(mid_xs)}")
