import cv2


def draw_point_history(img, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv2.circle(img, (int(point[0]), int(point[1])), 1 + int(index / 3), (152, 251, 152), 2)
