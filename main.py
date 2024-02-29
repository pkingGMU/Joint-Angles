# This script will take in webcam data (cv2) and use YOLO from ultraanylitics to draw a bio skeleton over the webcam footage. Joint positions will be used to determine relative angles

# Imports
import cv2
from ultralytics import YOLO
import numpy as np
import pprint
from pydantic import BaseModel

# Local Imports
import Base_Model

# Static Variables
saved_frames = []

# Base Model Class from pydantic
class GetKeypoint(BaseModel):

    NOSE:           int = 0
    LEFT_EYE:       int = 1
    RIGHT_EYE:      int = 2
    LEFT_EAR:       int = 3
    RIGHT_EAR:      int = 4
    LEFT_SHOULDER:  int = 5
    RIGHT_SHOULDER: int = 6
    LEFT_ELBOW:     int = 7
    RIGHT_ELBOW:    int = 8
    LEFT_WRIST:     int = 9
    RIGHT_WRIST:    int = 10
    LEFT_HIP:       int = 11
    RIGHT_HIP:      int = 12
    LEFT_KNEE:      int = 13
    RIGHT_KNEE:     int = 14
    LEFT_ANKLE:     int = 15
    RIGHT_ANKLE:    int = 16

# Use existing model for pose
model = YOLO('yolov8n-pose.pt')

## Video capture
# Initialized video capture from default camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set resolution
cap.set(3, 960) # Width
cap.set(4, 540) # Height

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

    # Press 1 to save a frame state and add it to the saved frames list
    elif key == ord('1'):
        saved_frames.append(model.predict(frame))

    # Write annotated frames to the output video if recording
    if recording:
        out.write(annotated_frame)

    # Exit the camera view
    if key == ord('q'):
        break
    
    #continue loop
    index += 1

# Release the video capture object and close all windows
if recording:
    out.release()
cap.release()
cv2.destroyAllWindows()


# Loop through saved frames and get keypoints for frames that are imported into numpy array
for frm in saved_frames:

    # If the information at the object 'frm' is equal to 'keypoints'
    if hasattr(frm[0], 'keypoints'):

        # local variable to store all keypoints
        keypoints = frm[0].keypoints

        #local variable to turn keypoints into a readable numpy array
        keypoints_numpy = keypoints.xyn.cpu().numpy()[0]

        #New instance of GetKeypoint
        get_keypoint = GetKeypoint()

        #Get nose coordinates
        nose_x, nose_y = keypoints_numpy[get_keypoint.NOSE]

        #print nose coordinates
        pprint.pprint(f'X: {nose_x} Y: {nose_y}')
    else:
        print('Didnt Work')

        

    

