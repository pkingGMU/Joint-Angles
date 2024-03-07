# This script will take in webcam data (cv2) and use YOLO from ultraanylitics to draw a bio skeleton over the webcam footage. Joint positions will be used to determine relative angles

# Imports
import cv2
from ultralytics import YOLO
import numpy as np
import os
import pandas as pd
import random


# Local Imports
import Base_Model
import Keypoints
import Client
import Vertical_Trunk

### Client information
## Find the next ID from the ROM.xlsx
# If ROM.xlsx exists
if os.path.exists('ROM.xlsx'):
    # Open the excel file into a dataframe
    existing_df = pd.read_excel('ROM.xlsx')
    # Check to make sure there is an ID column
    if 'ID' in existing_df:
        # Get our ID column
        id_column = existing_df['ID']
        # Make sure the column isn't empty
        if not id_column.empty:
            nextID = (existing_df['ID'].max()) + 1
        else:
            nextID = 1
    else:
        print("ID Column not found")

## TODO: Make an Input
# Randomly gets an age
random_age = random.randint(18, 40)

person = Client.Client(ID = nextID, age = random_age)

# Static Variables
saved_frames = []

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

    ## Check if camera is level
    # Check function
    level = Vertical_Trunk.webcam_level(frame)

    # Write text to screen
    text = "Level" if level else "Not level"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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

# Input our saved frames (should be top of motion then bottom of motion) and what we are looking for
results = Keypoints.Keypoints(saved_frames, ['TRUNK'])
# Input our person information into our dictionary
results['ID'] = person.id
results['AGE'] = person.age
# Console
print(results)

# Write results to excel workbook
# Excel file
if len(saved_frames) == 2:
    excel_file = "ROM.xlsx"

    # Check if the Excel file already exists
    if not os.path.exists(excel_file):
        # Create an empty DataFrame
        df = pd.DataFrame(columns=results.keys())  # Define columns as needed
    else:
        # Load existing Excel file into DataFrame
        df = pd.read_excel(excel_file)


    # Append the dictionary as a new row to the DF
    df.loc[len(df.index)] = results

    # Write the updata DataFram to the Excel File
    df.to_excel(excel_file, index=False)
        

    

