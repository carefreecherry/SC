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
