from flask import Flask, request, render_template, jsonify, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure the upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def count_sheets(image_path):
    try:
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise ValueError("Invalid image file")
        
        median_filtered = cv2.medianBlur(gray, 3)
        equalized = cv2.equalizeHist(median_filtered)
        edges = cv2.Canny(equalized, 90, 290)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=20, minLineLength=55, maxLineGap=5)
        
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

        if len(vertical_lines) > len(horizontal_lines):
            predominant_lines = vertical_lines
            direction = 'vertical'
        else:
            predominant_lines = horizontal_lines
            direction = 'horizontal'

        if direction == 'vertical':
            predominant_lines.sort()
        else:
            predominant_lines.sort()

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

        for coord in grouped_lines:
            if direction == 'vertical':
                cv2.line(image_with_lines, (coord, 0), (coord, image_with_lines.shape[0]), (0, 255, 0), 1)
            else:
                cv2.line(image_with_lines, (0, coord), (image_with_lines.shape[1], coord), (0, 255, 0), 1)

        processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], os.path.basename(image_path))
        cv2.imwrite(processed_image_path, image_with_lines)

        number_of_sheets = len(grouped_lines) - 1
        return number_of_sheets, processed_image_path
    except Exception as e:
        return str(e), None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        sheet_count, processed_image_path = count_sheets(file_path)
        
        if processed_image_path:
            return jsonify({'sheet_count': sheet_count, 'processed_image_path': processed_image_path})
        else:
            return jsonify({'error': sheet_count})  # error message from count_sheets function

    return jsonify({'error': 'Invalid file format'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
