Sheet Count detection
A web-based application for counting sheet stacks in manufacturing plants. Built with Flask, HTML/CSS, and OpenCV, it automates sheet counting by processing uploaded images, offering accurate and efficient results for industrial environments.

Table of Contents
Sheet Count detection
Table of Contents
Features
Prerequisites
Setup
Project Structure
Contributing
License

Features:
Automates the counting of sheet stacks in a manufacturing plant.
Uses computer vision techniques for accurate sheet count detection.
User-friendly web interface for uploading images and receiving sheet counts.
Optimized for performance to ensure quick responses.

Prerequisites
Python 3.8+
Flask
OpenCV
NumPy

Setup

Clone the repository:
git clone https://github.com/carefreecherry/SC

Set up a virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

''if error occurs while `.venv\Scripts\activate` then follow the below steps:
1) Open PowerShell as an Administrator: Right-click on the Start button and select "Windows PowerShell (Admin)" or "Windows Terminal (Admin)".
2) Check the current execution policy by running the following command:
Get-ExecutionPolicy
3) Change the execution policy to allow scripts to run. You can choose between different levels:

a) RemoteSigned: Allows scripts created on your machine to run, and scripts downloaded from the internet must be signed by a trusted publisher.
Set-ExecutionPolicy RemoteSigned
OR
b) Unrestricted: Allows all scripts to run.
To set the execution policy to RemoteSigned, run:
Set-ExecutionPolicy Unrestricted

4) You may be prompted to confirm the change. Type Y and press Enter to confirm.

5)After changing the execution policy, run the below command on your terminal:
.venv\Scripts\Activate


Install the required packages:
Check your Python version >=3.8.0

pip install Flask
pip install opencv-python
pip install matplotlib
pip install numpy

Run the Flask application:
python app.py
The backend will start on http://127.0.0.1:5000.

Project Structure

Sheet-counter/
├── Trails/                        
│   ├── 1_HoughTransform.py
│   ├── 2_MorphologicalClosing.py
│   ├── 3_Contouring.py
│   ├── 4_LineMidPoint.py.py
│   ├── 5_MLmodel
├── images/                             
│   ├── Video_frames                    
│   ├── sample images
├── static/       
│   ├──styles.css                     
│   ├──scripts.js                      
├── template/
│   ├──index.html                      # Frontend HTML file
├── processed/
├── uploads/
├── app.py
├── sheet_counter.py
├── Frames.py
├── README.md                          # This README file
├── Sheet_Counter                      # This PDF file
├── Working.mp4                        # This is Video

Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes.

License
This project is licensed under the MIT License.