# -*- coding: UTF-8 -*-

# 좌석 한 줄 별로 나누기 전에 가로 또는 길이 토대로 영역 판단해보기
# 좌석 분포 현황 분석하는 함수

def analyze_seat_wh(mhist):
    # 좌석의 가로(또는 세로) 덩어리 파악하기
    # 최소값 = 좌석 하나의 가로 또는 세로 길이
    min = -100  # 시작 좌표
    max = -100  # 끝 좌표
    min_length = -100
    seat = []
    for i in range(len(mhist)):
        # 좌석이 존재하는 좌표라면
        if (mhist[i] != 0):
            # min이 최초값이라면
            if (min < 0):
                min = i
            # max값 재조정
            if (max < i):
                max = i

        # 해당 좌표의 픽셀 개수가 0이라면
        else:
            # 하지만 min이 초기값이 아니면 - 좌석 덩어리 하나만큼 훑었다는 뜻
            if (min >= 0):
                length = max - min

                seat.append((length, min, max))

                if(min_length <= 0 or length < min_length):
                    min_length = length

                min = -100
                max = -100
        #print(i, min, max)

    # 좌석의 가로 좌표
    seat_length = min_length

    # 좌석의 가로 좌표보다 더 긴 좌석 분포는 따로 저장 (비정상 분포)
    longer = []
    for i in range(len(seat)):
        if(seat[i][0] > seat_length + 2):
            longer.append(seat[i])

    return seat_length, longer

# 빈 좌석 분포 확인하는 함수
def analyze_blank_wh(mhist):
    min_b = -100
    max_b = -100
    min_length = -100
    blank = []

    # 해당 좌표의 픽셀 개수가 0이라면
    for i in range(len(mhist)):
        if (mhist[i] == 0):
            # min_b가 최초값이라면
            if (min_b < 0):
                min_b = i
            # max값 재조정
            if (max_b < i):
                max_b = i

            # 이미지의 끝 여백 부분인 경우에 대한 처리
            if(min_b >= 0 and i==len(mhist)-1):
                b_length = max_b - min_b

                blank.append((b_length, min_b, max_b))

                if (min_length < 0 or b_length < min_length):
                    min_length = b_length

        else:
            # 하지만 min_b가 초기값이 아니면 - 빈공간 하나만큼 훑었다는 뜻
            if (min_b >= 0):
                b_length = max_b - min_b

                blank.append((b_length, min_b, max_b))

                if (min_length < 0 or b_length < min_length):
                    min_length = b_length

                min_b = -100
                max_b = -100


    # 좌석 간의 빈 공간보다 더 긴 빈 공간 분포는 따로 저장(비정상 분포)
    longer = []
    for i in range(len(blank)):
        if (blank[i][0] > min_length + 1):
            longer.append(blank[i])

    return longer

# 좌석 한 줄 별로 나누기
def seat_line(mhist_h):
    lines = []
    # 세로 줄 분석 - 좌석이 있는 좌표 파악
    for i in range(1, len(mhist_h)):
        if(mhist_h[i]!=0):
            if(i==1 and mhist_h[i-1]!=0):
                lines.append(0)
            elif(mhist_h[i-1]==0):
                lines.append(i)


    return lines

# 줄 별로 행렬 만들기
def define_matrix(mimage_w, seat_w):
    w = mimage_w
    matrix = [0] * (int(w / seat_w))

    return matrix

# 이미지 영역 내에서 좌석 line의 영역 잡기
def set_line_roi(lines, h):
    y_points = []
    min_y = -100
    max_y = -100
    for i in range(len(lines)):
        min_y = lines[i]
        max_y = lines[i] + h

        y_points.append((min_y, max_y))

    return y_points
