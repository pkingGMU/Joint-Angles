# This script will take in webcam data (cv2) and use YOLO from ultraanylitics to draw a bio skeleton over the webcam footage. Joint positions will be used to determine relative angles

# Imports
import cv2
from ultralytics import YOLO
import numpy as np

# Static Variables
saved_frames = []

## Functions
# Function to plot boxes


# Use existing model
model = YOLO('yolov8n-pose.pt')

## Video capture
# Initialized video capture from default camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set resolution
cap.set(3, 480) # Width
cap.set(4, 270) # Height

# Ensures video is opened correctly
assert cap.isOpened()

# Get the width, height, and fps of the video
w, h, fps = (int(cap.get(x)) for x in (
    cv2.CAP_PROP_FRAME_WIDTH, 
    cv2.CAP_PROP_FRAME_HEIGHT, 
    cv2.CAP_PROP_FPS
    ))

# Define the codec for the output
fourcc = cv2.VideoWriter_fourcc('a','v','c','i')

#Initialize the VideoWriter object for recording (None for right now)
out = None
# Recording state false
recording = False
# Index variable
index = 0

# Loop to capture frames and display them
while cap.isOpened():
    # Read a frame from the cameera
    success, frame = cap.read()
    if not success:
        print("Error")
        break
    # Use frame to determine model annotation
    annotation = model.predict(frame, classes=0)
    if index == 1:
        saved_frames.append(annotation.numpy())

    # Overaly the annotation onto the webcam view
    annotated_frame = annotation[0].plot(labels=True, boxes=False, conf=1.0)
    
    # Display the frame with annotated overlay
    cv2.imshow('Camera View', annotated_frame)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF

    # Start recording
    if key == ord('r') and not recording:
        out = cv2.VideoWriter(f'output{index}.mp4', fourcc, fps, (w, h))
        recording = True
        print("Recording started")
    
    # Stop recording
    elif key == ord('s') and recording:
        recording = False
        out.release()
        print("Recording stopped")
        index += 1

    # Write annotated frames to the output video if recording
    if recording:
        out.write(annotated_frame)

    # Exit the camera view
    if key == ord('q'):
        break

    index += 1

# Release the video capture object and close all windows
if recording:
    out.release()
cap.release()
cv2.destroyAllWindows()

print(saved_frames)
    


