import Base_Model
import numpy as np
import Degree_Calculation

# What we want to return later
results = {
    'TrunkROM': None,
    'RIGHT HIP ROM': None,
    'LEFT HIP ROM': None,
    'RIGHT KNEE ROM': None,
    'LEFT KNEE ROM': None,
    'AnkleROM': None,
    'RIGHT SHOULDER FLEXION ROM': None,
    'LEFT SHOULDER FLEXION ROM': None

}

# List of each angle for each frame
tempTrunk = []
temp_knee_right = []
temp_knee_left = []
temp_hip_right = []
temp_hip_left = []
tempAnkle = [] 
temp_right_shoulder_flexion = []
temp_left_shoulder_flexion = []

def Keypoints(saved_frame_list, joint_angle_desired: list):

    # Iterate through each joint_angle_desired
    for joint in joint_angle_desired:

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

                    # Get all points for the frame 
                    nose = keypoints_numpy[get_keypoint.NOSE]
                    left_eye = keypoints_numpy[get_keypoint.LEFT_EYE]
                    right_eye = keypoints_numpy[get_keypoint.RIGHT_EYE]
                    left_ear = keypoints_numpy[get_keypoint.LEFT_EAR]
                    right_ear = keypoints_numpy[get_keypoint.RIGHT_EAR]
                    left_shoul = keypoints_numpy[get_keypoint.LEFT_SHOULDER]
                    right_shoul = keypoints_numpy[get_keypoint.RIGHT_SHOULDER]
                    left_elbow = keypoints_numpy[get_keypoint.LEFT_ELBOW]
                    right_elbow = keypoints_numpy[get_keypoint.RIGHT_ELBOW]
                    left_wrist = keypoints_numpy[get_keypoint.LEFT_WRIST]
                    right_wrist = keypoints_numpy[get_keypoint.RIGHT_WRIST]
                    left_hip = keypoints_numpy[get_keypoint.LEFT_HIP]
                    right_hip = keypoints_numpy[get_keypoint.RIGHT_HIP]
                    left_knee = keypoints_numpy[get_keypoint.LEFT_KNEE]
                    right_knee = keypoints_numpy[get_keypoint.RIGHT_KNEE]
                    left_ankle = keypoints_numpy[get_keypoint.LEFT_ANKLE]
                    right_ankle = keypoints_numpy[get_keypoint.RIGHT_ANKLE]

                    # Get X,Y coordinates for the appropriate angle desired
                    match joint:

                        case 'TRUNK':
                            pass

                        case 'RIGHT KNEE':
                            temp_knee_right.append(Degree_Calculation.degrees(right_hip,right_knee,right_ankle))
                        case 'LEFT KNEE':
                            temp_knee_left.append(Degree_Calculation.degrees(left_hip,left_knee,left_ankle))
                        case 'RIGHT HIP':
                            temp_hip_right.append(Degree_Calculation.degrees(nose,right_hip,right_knee))
                        case 'LEFT HIP':
                            temp_hip_right.append(Degree_Calculation.degrees(nose,left_hip,left_knee))
                        case 'ANKLE':
                            pass
                        case 'RIGHT SHOULDER FLEXION':
                            temp_right_shoulder_flexion.append(Degree_Calculation.degrees(right_wrist,right_shoul,right_hip))
                        case 'RIGHT SHOULDER FLEXION':
                            temp_left_shoulder_flexion.append(Degree_Calculation.degrees(left_wrist,left_shoul,left_hip))
            
            match joint:
                case 'TRUNK':
                    pass

                case 'RIGHT KNEE':
                    results['RIGHT KNEE ROM'] = temp_knee_right[0] - temp_knee_right[1]
                case 'LEFT KNEE':
                    results['LEFT KNEE ROM'] = temp_knee_left[0] - temp_knee_left[1]
                case 'RIGHT HIP':
                    results['RIGHT HIP ROM'] = temp_hip_right[0] - temp_hip_right[1]
                case 'LEFT HIP':
                    results['LEFT HIP ROM'] = temp_hip_left[0] - temp_hip_left[1]
                case 'ANKLE':
                    pass
                case 'RIGHT SHOULDER FLEXION':
                    results['RIGHT SHOULDER FLEXION ROM'] = temp_right_shoulder_flexion[1]-temp_right_shoulder_flexion[0]     
                case 'RIGHT SHOULDER FLEXION':
                    results['LEFT SHOULDER FLEXION ROM'] = temp_left_shoulder_flexion[1] - temp_left_shoulder_flexion[0]
                           
        else:
            return 'You need two saved frames'







        

    return results

            



            