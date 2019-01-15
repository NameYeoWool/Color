# -*- coding: UTF-8 -*-

def occupied_in_grid(seat_w, start_x, end_x, obj_x, obj_w):
    # 검사할 grid의 좌표 범위
    x_range = set(range(start_x, end_x))
    # 검사할 개체의 좌표 범위
    obj_x_range = list(range(obj_x, obj_w))
    # 격자 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in obj_x_range if value in x_range]

    if len(intersect_x) >= seat_w / 1.5 :
        return True
    else:
        return False

def emptyseat_in_grid(seat_w, seat_h, x, y, obj_x, obj_y, obj_w, obj_h):
    # 검사할 grid의 좌표 범위
    x_range = set(range(x, x + seat_w + 1))
    y_range = set(range(y, y + seat_h + 1))
    # 검사할 개체의 좌표 범위
    obj_x_range = list(range(obj_x, obj_w))
    obj_y_range = list(range(obj_y, obj_h))
    # 격자 한 칸과 타겟의 x,y좌표 겹치는 것 찾기
    intersect_x = [value for value in obj_x_range if value in x_range]
    intersect_y = [value for value in obj_y_range if value in y_range]

    if len(intersect_x) >= seat_w / 1.5 and len(intersect_y) >= seat_h / 1.5:
        return True
    else:
        return False


def seat_collision(matrix, seat_w, pimage_w, occupied_list, empty_list):
    interval = int(pimage_w / len(matrix))
    points = [0]
    p = 0
    for i in range(len(matrix)):
        p = p + interval
        points.append(p)

    for ver in range(len(matrix)):
        for occ_seat in occupied_list:
            x, y, w, h = occ_seat   #seat_w, x, obj_x, obj_w
            if occupied_in_grid(seat_w, points[ver], points[ver+1], x, x+w):
                # 해당 되는 좌표 위치에 matrix 값을 업데이트 한다
                matrix[ver] = 2  # 차지한 좌석

        for emp_seat in empty_list:
            x, y, w, h = emp_seat
            if occupied_in_grid(seat_w, points[ver], points[ver+1], x, x+w):
                # 해당 되는 좌표 위치에 matrix 값을 업데이트 한다
                matrix[ver] = 1  # 빈 좌석

    return matrix
