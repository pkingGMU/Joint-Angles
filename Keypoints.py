import Base_Model
import numpy as np
import Degree_Calculation


def get_keypoints(saved_frame):
    if hasattr(saved_frame[0], 'keypoints'):
        keypoints = saved_frame[0].keypoints
        keypoints_numpy = keypoints.xyn.cpu().numpy()[0]
        return keypoints_numpy
    return None


def calculate_angles(joint, keypoints):
    print(keypoints[Base_Model.GetKeypoint().NOSE])
    print([(keypoints[Base_Model.GetKeypoint().RIGHT_HIP])[0], 0])

    if joint == 'TRUNK':
        return Degree_Calculation.degrees([(keypoints[Base_Model.GetKeypoint().RIGHT_HIP])[0], 0],
                                          keypoints[Base_Model.GetKeypoint().RIGHT_HIP],
                                          keypoints[Base_Model.GetKeypoint().RIGHT_EAR]
                                          )
    elif joint == 'RIGHT KNEE':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().RIGHT_HIP],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_KNEE],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_ANKLE])
    elif joint == 'LEFT KNEE':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().LEFT_HIP],
                                        keypoints[Base_Model.GetKeypoint().LEFT_KNEE],
                                        keypoints[Base_Model.GetKeypoint().LEFT_ANKLE])
    elif joint == 'RIGHT HIP':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().RIGHT_EAR],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_HIP],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_KNEE])
    elif joint == 'LEFT HIP':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().LEFT_EAR],
                                        keypoints[Base_Model.GetKeypoint().LEFT_HIP],
                                        keypoints[Base_Model.GetKeypoint().LEFT_KNEE])
    elif joint == 'ANKLE':
        return None
    elif joint == 'RIGHT SHOULDER FLEXION':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().RIGHT_WRIST],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_SHOULDER],
                                        keypoints[Base_Model.GetKeypoint().RIGHT_HIP])
    elif joint == 'LEFT SHOULDER FLEXION':
        return Degree_Calculation.degrees(keypoints[Base_Model.GetKeypoint().LEFT_WRIST],
                                        keypoints[Base_Model.GetKeypoint().LEFT_SHOULDER],
                                        keypoints[Base_Model.GetKeypoint().LEFT_HIP])
    else:
        return None
    

def calculate_rom(joint, angles, results):
    if joint == 'RIGHT KNEE':
        results['RIGHT KNEE ROM'] = angles[0] - angles[1]
    elif joint == 'LEFT KNEE':
        results['LEFT KNEE ROM'] = angles[0] - angles[1]
    elif joint == 'RIGHT HIP':
        results['RIGHT HIP ROM'] = angles[0] - angles[1]
    elif joint == 'LEFT HIP':
        results['LEFT HIP ROM'] = angles[0] - angles[1]
    elif joint == 'RIGHT SHOULDER FLEXION':
        results['RIGHT SHOULDER FLEXION ROM'] = angles[1] - angles[0]
    elif joint == 'LEFT SHOULDER FLEXION':
        results['LEFT SHOULDER FLEXION ROM'] = angles[1] - angles[0]
    elif joint == 'TRUNK':
        results['TRUNK ROM'] = angles[1] - angles[0]


def Keypoints(saved_frame_list, joint_angle_desired: list):
    """
    Function to process the saved frame list and calculate joint angles
    """
    # Dictionary to store the results
    results = {}

    # Iterate through each joint desired
    for joint in joint_angle_desired:

        # Create an empty list to store the angles for the current joint
        temp_angles = []

        # Iterate  through each frame
        for frame in saved_frame_list:

            # Get the keypoints from the current frame
            keypoints = get_keypoints(frame)
            print(keypoints)

            # Calculate the angles for the current joint
            angle = calculate_angles(joint, keypoints)
            # Append ange to the list if it doesn't return None
            if angle is not None:
                temp_angles.append(angle)
        print(f"For joint '{joint}', temp_angles: {temp_angles}")  # Debugging line
        # Calculate range of motion with our two angles for each joint
        if len(temp_angles) == 2:
            calculate_rom(joint, temp_angles, results)
        else:
            return 'You need two saved frames'
    return results

            



            