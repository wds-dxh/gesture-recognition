import copy
import itertools


def landmark_handle(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)
    deal = [[1, 0], [2, 1], [3, 1], [4, 1], [5, 0], [6, 5], [7, 5], [8, 5], [9, 0], [10, 9], [11, 9], [12, 9], [13, 0],
            [14, 13] , [15, 13], [16, 13], [17, 0], [18, 17], [19, 17], [20, 17], [4, 12], [8, 12], [16, 20], [20, 12]]
    for index, way in enumerate(deal):
        a = temp_landmark_list[way[0]][0] - temp_landmark_list[way[1]][0]
        b = temp_landmark_list[way[0]][1] - temp_landmark_list[way[1]][1]
        deal[index][0] = a
        deal[index][1] = b

    deal = list(
        itertools.chain.from_iterable(deal))

    max_value = max(list(map(abs, deal)))

    def normalize_(n):
        return n / max_value

    deal = list(map(normalize_, deal))

    return deal
