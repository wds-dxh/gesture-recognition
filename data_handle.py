import cv2
import mediapipe as mp
import numpy as np
from tools.landmark_handle import landmark_handle

video_num = 1
# 三个人的效果没有一个人的好，还在想办法

label = ["also", "attractive", "beautiful", "believe", "de", "doubt", "dream", "express", "eye", "give", "handLang",
         "have",
         "many",
         "me", "method", "no", "only", "over", "please", "put", "say", "smile", "star", "use_accept_give", "very",
         "watch",
         "you"]
label_num = len(label)
print("label_num:" + str(label_num))
# 模型保存地址即是label+.npz
# video_path即是label+_

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75)

for i in range(len(label)):
    print(str(i + 1) + "/" + str(len(label)) + ":" + label[i])
    data = []
    for j in range(video_num):
        # cap = cv2.VideoCapture("./Video/static/" + label[i] + "_" + str(j) + ".mp4")
        cap = cv2.VideoCapture("./Video/static/" + label[i] + "_" + "1" + ".mp4")
        ret, frame = cap.read()
        while ret is True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            results = hands.process(frame)#
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    hand_local = []
                    for ix in range(21):
                        x = min(int(hand_landmarks.landmark[ix].x * frame.shape[1]), frame.shape[1] - 1)
                        y = min(int(hand_landmarks.landmark[ix].y * frame.shape[0]), frame.shape[0] - 1)
                        hand_local.append([x, y])
                    hand_local = landmark_handle(hand_local)
                    data.append(hand_local)

            ret, frame = cap.read()

    np.savez_compressed("./npz_files/" + label[i] + ".npz", data=data)
