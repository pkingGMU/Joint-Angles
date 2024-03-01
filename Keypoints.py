import Base_Model
import numpy as np
import Degree_Calculation

# What we want to return later
results = {
    'TrunkROM': None,
    'HipROM': None,
    'KneeROM': None,
    'AnkleROM': None
}

# List of each angle for each frame
tempTrunk = []
temp_knee_right = []
temp_knee_left = []
tempAnkle = [] 

def Keypoints(saved_frame_list, joint_angle_desired):
    # Checks for two saved frames
    if len(saved_frame_list) == 2:
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
                        temp_knee_right.append(Degree_Calculation.degrees(right_hip,right_knee,right_ankle))
                    case 'LEFT KNEE':
                        left_hip = keypoints_numpy[get_keypoint.LEFT_HIP]
                        left_knee = keypoints_numpy[get_keypoint.LEFT_KNEE]
                        left_ankle = keypoints_numpy[get_keypoint.LEFT_ANKLE]
                        temp_knee_left.append(Degree_Calculation.degrees(left_hip,left_knee,left_ankle))
                    case 'ANKLE':
                        pass
        
        match joint_angle_desired:
            case 'TRUNK':
                pass

            case 'RIGHT KNEE':
                results['KneeROM'] = temp_knee_right[0] - temp_knee_right[1]
            case 'LEFT KNEE':
                results['KneeROM'] = temp_knee_left[0] - temp_knee_left[1]
            case 'ANKLE':
                pass
    else:
        return 'You need two saved frames'







    

    return results

            



            