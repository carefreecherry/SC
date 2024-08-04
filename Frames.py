'''To enhance your dataset, consider extracting additional frames from your sample video. 
You can use OpenCV's extract_frames function to read the video and save frames at specified 
intervals. By adjusting the frame rate, you can control how frequently frames are captured, 
allowing you to generate more data from a single video. This approach is especially useful for 
expanding small datasets and can provide a more diverse range of data for analysis or training.'''

import cv2
import os

# Function to extract frames from video
def extract_frames(video_path, output_folder, frame_rate=1):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    while success:
        if count % frame_rate == 0:
            cv2.imwrite(os.path.join(output_folder, f"frame{count}.jpg"), image)
        success, image = vidcap.read()
        count += 1

# Example usage
video_path = 'images/Sample Video.mp4'
output_folder = 'images/Video_Frames/'
extract_frames(video_path, output_folder, frame_rate=20)  # Extract every 20th frame
