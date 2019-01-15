# -*- coding: UTF-8 -*-
def matrix_to_num(matrix):
    # bit_num을 0으로 설정하면,
    #  맨 처음에 01을 넣지 않고 그냥 1만 넣기에 '총 자리 수'에 문제 발생
    # 이를 해결하기 위해 그냥 초기 값은 1로 둔다
    bit_num = 1
    #비트에는 matrix 배열 '역순'으로 넣기 시작한다
    for i in range(len(matrix)-1, -1, -1):
        if matrix[i] == 0:
            tmp = 1
            bit_num = bit_num << 2
            bit_num = bit_num + tmp

        elif matrix[i] == 1:
            tmp = 2
            bit_num = bit_num << 2
            bit_num = bit_num + tmp

        elif matrix[i] == 2:
            tmp = 3
            bit_num = bit_num << 2
            bit_num = bit_num + tmp

    return bit_num # unsigned long 숫자

def starting_point(area_num, roi_points, y_point):
    x_points = []
    for i in range(len(roi_points)):
        if(i%2==0):
            x_points.append(roi_points[i][0])

    return x_points[area_num], y_point


def num_to_matrix(bit_num, matrix):
    state_matrix = []
    # bit 수는 g.vertical_max + 1 만큼이다
    for i in range(len(matrix)):
    # 임시 수: 기존 수에 맨 끝에 2자리 bit를 00로 리셋
        tmp_num = bit_num >> 2
        tmp_num = tmp_num << 2
        #print("tmp num: ", bin(tmp_num))

        # 기존 수 - 임시 수 = 끝 2 bit의 차이
        # 즉, 마지막 2 bit 값을 구할 수 있다
        tmp = bit_num - tmp_num

        # 기존 matrix state 로 환원하는 과정
        if tmp == 1:
            num = 0
        elif tmp == 2:
            num = 1
        elif tmp == 3:
            num = 2

        # 새 matrix에 삽입
        state_matrix.append(num)

        # 이미 판별한 마지막 2 bit는 더 이상 필요없으므로 삭제
        bit_num = bit_num >> 2

    return state_matrix
