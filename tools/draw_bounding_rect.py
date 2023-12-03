import numpy as np
import cv2


def draw_bounding_rect(image, landmarks_point):
    x, y, w, h = cv2.boundingRect(np.array(landmarks_point))
    brect = [x, y, x + w, y + h]
    cv2.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                  (0, 0, 0), 1)

    return brect
