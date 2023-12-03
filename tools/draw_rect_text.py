import cv2

def draw_rect_txt(frame, info_text,brect):
    cv2.putText(frame, info_text, (brect[0] + 5, brect[1] - 4),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
