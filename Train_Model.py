import cv2
import mediapipe as mp
import numpy as np
import time
import pandas as pd

def dump_points(pointArray, fileName):
    print(len(pointArray))
    data = pd.DataFrame(data=pointArray, columns=keyXYZ, index=None)
    data.to_csv(fileName, encoding='utf-8',index=False)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
prevTime = 0
keyPoint = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index"
]
keyXYZ = [
    "class",
    "nose_x",
    "nose_y",
    "nose_z",
    "left_eye_inner_x",
    "left_eye_inner_y",
    "left_eye_inner_z",
    "left_eye_x",
    "left_eye_y",
    "left_eye_z",
    "left_eye_outer_x",
    "left_eye_outer_y",
    "left_eye_outer_z",
    "right_eye_inner_x",
    "right_eye_inner_y",
    "right_eye_inner_z",
    "right_eye_x",
    "right_eye_y",
    "right_eye_z",
    "right_eye_outer_x",
    "right_eye_outer_y",
    "right_eye_outer_z",
    "left_ear_x",
    "left_ear_y",
    "left_ear_z",
    "right_ear_x",
    "right_ear_y",
    "right_ear_z",
    "mouth_left_x",
    "mouth_left_y",
    "mouth_left_z",
    "mouth_right_x",
    "mouth_right_y",
    "mouth_right_z",
    "left_shoulder_x",
    "left_shoulder_y",
    "left_shoulder_z",
    "right_shoulder_x",
    "right_shoulder_y",
    "right_shoulder_z",
    "left_elbow_x",
    "left_elbow_y",
    "left_elbow_z",
    "right_elbow_x",
    "right_elbow_y",
    "right_elbow_z",
    "left_wrist_x",
    "left_wrist_y",
    "left_wrist_z",
    "right_wrist_x",
    "right_wrist_y",
    "right_wrist_z",
    "left_pinky_x",
    "left_pinky_y",
    "left_pinky_z",
    "right_pinky_x",
    "right_pinky_y",
    "right_pinky_z",
    "left_index_x",
    "left_index_y",
    "left_index_z",
    "right_index_x",
    "right_index_y",
    "right_index_z",
    "left_thumb_x",
    "left_thumb_y",
    "left_thumb_z",
    "right_thumb_x",
    "right_thumb_y",
    "right_thumb_z",
    "left_hip_x",
    "left_hip_y",
    "left_hip_z",
    "right_hip_x",
    "right_hip_y",
    "right_hip_z",
    "left_knee_x",
    "left_knee_y",
    "left_knee_z",
    "right_knee_x",
    "right_knee_y",
    "right_knee_z",
    "left_ankle_x",
    "left_ankle_y",
    "left_ankle_z",
    "right_ankle_x",
    "right_ankle_y",
    "right_ankle_z",
    "left_heel_x",
    "left_heel_y",
    "left_heel_z",
    "right_heel_x",
    "right_heel_y",
    "right_heel_z",
    "left_foot_index_x",
    "left_foot_index_y",
    "left_foot_index_z",
    "right_foot_index_x",
    "right_foot_index_y",
    "right_foot_index_z"
]
print(len(keyXYZ))
res_point = []
normal_points = []
fall_points = []
print(len(keyPoint))
cap = cv2.VideoCapture("Fall_Trim.mp4")
with mp_pose.Pose(
        static_image_mode=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks:
            res_point.append(1) # the class 0 mean fall, 1 means normal. Please ref the fall_point.csv
            for index, landmarks in enumerate(results.pose_landmarks.landmark):
                # print(keyPoint[index], landmarks.x, landmarks.y, landmarks.z)
                # print(len(results.pose_landmarks.landmark))
                res_point.append(landmarks.x)
                res_point.append(landmarks.y)
                res_point.append(landmarks.z)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
        # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        cv2.imshow('MediaPipe Pose', image)

        userInput = cv2.waitKey(0) & 0xFF
        if  userInput == ord('q'):
            dump_points(normal_points, "normal_point.csv")
            dump_points(fall_points, "fall_point.csv")

            break
        if userInput == ord('y'):
            res_point[0] = 1
            # print(res_point)
            normal_points.append(res_point.copy())

        if userInput == ord('n'):
            res_point[0] = 0
            # print(res_point)
            fall_points.append(res_point.copy())

        res_point.clear()
cap.release()


