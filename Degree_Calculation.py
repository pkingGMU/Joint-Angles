# Calculate all three degrees of a joint triangle

# Imports
import numpy as np

def degrees(A, B, C):
    # Calculate angles
    e1 = B-A; e2 = C-A
    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
    d1 = np.rad2deg(np.arccos(np.dot(e1, e2)/denom))

    e1 = C-B; e2 = A-B
    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
    d2 = np.rad2deg(np.arccos(np.dot(e1, e2)/denom))

    d3 = 180-d1-d2

    return d2