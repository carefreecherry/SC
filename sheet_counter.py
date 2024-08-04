'''The sheet counter approach begins with preprocessing the image by converting it to grayscale, 
applying median filtering, and using histogram equalization for better contrast. Edge detection 
with the Canny edge detector highlights the sheet boundaries, followed by detecting lines using 
the Hough Line Transform. Detected lines are classified as vertical or horizontal, sorted, and 
grouped based on proximity. Representative lines are then drawn on the original image to visualize 
the sheet boundaries, and the number of sheets is calculated by counting these lines. '''

import cv2
import numpy as np
import os

def count_sheets(image_path):
    try:
        # Load the image in grayscale
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise ValueError("Invalid image file")
        
        # Preprocess the image
        median_filtered = cv2.medianBlur(gray, 3)
        equalized = cv2.equalizeHist(median_filtered)
        edges = cv2.Canny(equalized, 90, 290)
        
        # Detect lines using Hough Line Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=55, maxLineGap=5)
        
        # Load the original image to draw lines on it
        image_with_lines = cv2.imread(image_path)
        vertical_lines = []
        horizontal_lines = []

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(x1 - x2) < 6:
                    vertical_lines.append((x1, min(y1, y2), max(y1, y2)))
                elif abs(y1 - y2) < 6:
                    horizontal_lines.append((y1, min(x1, x2), max(x1, x2)))

        # Determine the predominant direction of the lines
        if len(vertical_lines) > len(horizontal_lines):
            predominant_lines = vertical_lines
            direction = 'vertical'
        else:
            predominant_lines = horizontal_lines
            direction = 'horizontal'

        # Sort the lines based on their coordinates
        predominant_lines.sort()

        # Group nearby lines together
        grouped_lines = []
        group_threshold = 3
        current_group = []

        for coord, min_pos, max_pos in predominant_lines:
            if not current_group or abs(coord - current_group[-1][0]) <= group_threshold:
                current_group.append((coord, min_pos, max_pos))
            else:
                representative_coord = max(current_group, key=lambda item: item[2])[0]
                grouped_lines.append(representative_coord)
                current_group = [(coord, min_pos, max_pos)]

        if current_group:
            representative_coord = max(current_group, key=lambda item: item[2])[0]
            grouped_lines.append(representative_coord)

        # Draw the grouped lines on the image
        for coord in grouped_lines:
            if direction == 'vertical':
                cv2.line(image_with_lines, (coord, 0), (coord, image_with_lines.shape[0]), (0, 255, 0), 1)
            else:
                cv2.line(image_with_lines, (0, coord), (image_with_lines.shape[1], coord), (0, 255, 0), 1)

        # Save the processed image
        processed_image_path = os.path.join('processed', os.path.basename(image_path))
        cv2.imwrite(processed_image_path, image_with_lines)

        # Calculate the number of sheets
        number_of_sheets = len(grouped_lines) - 1
        return number_of_sheets, processed_image_path
    except Exception as e:
        return str(e), None
