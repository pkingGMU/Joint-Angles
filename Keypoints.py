import Base_Model
import Distance_Between_Points
import numpy as np

results = []

def Keypoints(saved_frame_list, joint_angle_desired):
    # Loop through saved frames and get keypoints for frames that are imported into numpy array
    for frm in saved_frame_list:

        # If the information at the object 'frm' is equal to 'keypoints'
        if hasattr(frm[0], 'keypoints'):

            # local variable to store all keypoints
            keypoints = frm[0].keypoints

            # local variable to turn keypoints into a readable numpy array
            keypoints_numpy = keypoints.xyn.cpu().numpy()[0]

            # New instance of GetKeypoint
            get_keypoint = Base_Model.GetKeypoint()

            # Get X,Y coordinates for the appropriate angle desired
            match joint_angle_desired:

                case 'TRUNK':
                    pass

                case 'RIGHT KNEE':
                    right_hip = keypoints_numpy[get_keypoint.RIGHT_HIP]
                    right_knee = keypoints_numpy[get_keypoint.RIGHT_KNEE]
                    right_ankle = keypoints_numpy[get_keypoint.RIGHT_ANKLE]
                    
                    # Calculate angles
                    e1 = right_knee-right_hip; e2 = right_ankle-right_hip
                    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
                    d1 = np.rad2deg(np.arccos(np.dot(e1, e2)/denom))

                    e1 = right_ankle-right_knee; e2 = right_hip-right_knee
                    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
                    d2 = np.rad2deg(np.arccos(np.dot(e1, e2)/denom))

                    d3 = 180-d1-d2

                    print (f' Dont care: {d1}, Angle of Knee for frame: {d2}, Dont care{d3}')

                case 'HIP':
                    pass
                case 'ANKLE':
                    pass

            



            