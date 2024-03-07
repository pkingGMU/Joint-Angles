## Receive a frame from the camera and determine if the camera is level

# Imports
import cv2
import numpy as np

def webcam_level(frame) -> bool:
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply edge detection (Canny edge detector)
    edges = cv2.Canny(gray, 50, 150)

    # Find lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # Just in case lines return None (It doesn't see any lines)
    if lines is None:
        return False

    # Calculate the angles of lines with respect to horizontal
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        angles.append(angle)
   
        
    # Determine the average angle
    avg_angle = np.mean(angles)
    
    # Check if the average angle is within a threshold
    threshold = 10  # Set your desired threshold
    if abs(avg_angle) < threshold:
        return True  # Camera is level
    else:
        return False  # Camera is not level


