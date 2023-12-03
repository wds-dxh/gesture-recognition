def landmark_dynamic_handle(landmark_list):
    frames = len(landmark_list)
    landmark_list_new = []
    for i in range(frames - 1):
        landmark_list_new.append(
            [landmark_list[i + 1][0] - landmark_list[i][0], landmark_list[i + 1][1] - landmark_list[i][1]])
    return landmark_list_new
