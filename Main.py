# -*- coding: UTF-8 -*-
import cv2
import numpy as np
import requests
from graphics import *
from random import *
from PIL import Image, ImageDraw

import Histogram2 as h, Decide_matrix2 as dm, Image_partitioning as ip, Color_detect2 as cd, \
    Grid2 as g, Bit2 as b
import json


def json_convert(seats):
    # 받아온 딕셔너리로 json파일 생성하는 함수
    fj = open("pc_info.json", "w")
    jsonString = json.dumps(seats, ensure_ascii=False)
    requests.post('http://13.209.122.73:8000/save/', # 13.209.122.73
                  data={'data': jsonString, 'pc_room': '세븐 PC방'},
                  files={'seat_image': open('convert.gif', 'rb')})
    fj.write(jsonString)
    fj.close()


def main():
    # 분석할 pc방 좌석도 가져오기
    image = cv2.imread("screen_shot.png")
    # cv2.line(image, (427, 0), (427, 50), (255, 0, 0), 2)
    # cv2.imshow("pcroom", image)
    totalSeatNum = 0
    emptySeatNum = 0

    # json 파일 만들기 위한 dictionary
    dic_for_json = {}
    seats = []

    f = open("test.txt", 'w')
    fc = open("convert.txt", 'w')

    # image의 size
    image_h, image_w = image.shape[:2]
    f.write("%d %d\n" % (image_h, image_w))
    fc.write("%d %d\n" % (image_h, image_w))
    dic_for_json["image_h"] = image_h
    dic_for_json["image_w"] = image_w
    # print(image_w, image_h)

    # 분석을 위해 이미지 가공
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    # cv2.imshow("f", thresh)

    # 전체 histogram 분석 먼저한다
    hist_w, mhist_w = h.histogram(thresh, 0, image_w, image_h)  # height
    hist_h, mhist_h = h.histogram(thresh, 1, image_w, image_h)  # width

    # <Decide_matrix2>

    # 1. 좌석 한 개의 가로, 세로 길이 구하기 + 좌석 분포가 비정상인 경우 추출(=여러 좌석이 뭉쳐서 나타나는 경우)
    seat_w, innormal_w = dm.analyze_seat_wh(mhist_w)
    seat_h, innormal_h = dm.analyze_seat_wh(mhist_h)

    f.write("%d %d\n" % (seat_w, seat_h))
    fc.write("%d %d\n" % (seat_w, seat_h))

    dic_for_json["seat_h"] = seat_h
    dic_for_json["seat_w"] = seat_w

    # 2. 빈 공간의 분포가 넓은 부분 추출해내기
    blanks_w = dm.analyze_blank_wh(mhist_w)
    blanks_h = dm.analyze_blank_wh(mhist_h)

    # 3. 빈 공간의 분포를 기준으로 하여 영역 별로 이미지 쪼개기
    roi_points = ip.image_partition(image, blanks_w, blanks_h)
    # print(roi_points)   # roi_points = 한 영역의 가장 끝과 끝 좌표(한 영역 당 2쌍)

    image_parts = []
    for i in range(int(len(roi_points) / 2)):  # for문: 이미지 영역의 갯수
        # 쪼개려는 부분의 좌표를 통해 이미지 영역 분할
        pimage = ip.set_roi(image, roi_points[i * 2], roi_points[i * 2 + 1])  # 전체 이미지, x좌표, y좌표
        image_parts.append(pimage)  # 쪼개진 이미지 영역 보관

        # cv2.imshow("pimage", pimage)
        # cv2.waitKey(0)

        # 기존 이미지의 threshold 역시 같은 규격으로 분할한다.
        pthresh = ip.set_roi(thresh, roi_points[i * 2], roi_points[i * 2 + 1])

        # 쪼개진 이미지 영역의 histogram을 추가로 추출
        pimage_h, pimage_w = pimage.shape[:2]  # 분할한 이미지 영역의 사이즈
        phist_w, pmhist_w = h.histogram(pthresh, 0, pimage_w, pimage_h)  # height
        phist_h, pmhist_h = h.histogram(pthresh, 1, pimage_w, pimage_h)  # width

        # 좌석 라인 별로 나누기
        # line 위치 파악
        lines = dm.seat_line(pmhist_h)  # 이미지 영역에서 추출한 좌석 line들의 위치
        y_points = dm.set_line_roi(lines, seat_h)  # line의 시작, 끝 y좌표점

        # 영역 이미지 내에서 이제 좌석 line 하나씩 분석한다
        for j in range(len(y_points)):
            seat_list = []

            # line 별로 이미지, thresh 나누기
            roi_img = cd.cut_roi(pimage, y_points[j][0], y_points[j][1], pimage_w)
            roi_thresh = cd.cut_roi(pthresh, y_points[j][0], y_points[j][1], pimage_w)

            # thresh 이미지 통해 좌석 개체 좌표 획득
            seat_list = cd.seat_detect(roi_thresh, seat_w, seat_h)

            # 좌석 개체 좌표에 해당하는 부분 색상분석
            occupied_list, empty_list = cd.seat_color_detect(roi_img, seat_list, seat_w, seat_h)

            print(seat_list)
            start_x = seat_list[0][0]  # 해당 좌석 시작하는 x 좌표
            # matrix 선언
            # roi_matrix = dm.define_matrix(pmhist_w, start_x, seat_w)
            roi_matrix = dm.define_matrix(pimage_w, seat_w)

            # matrix 영역 안에 개체 리스트가 존재하는지 확인
            # roi_matrix = g.seat_collision(roi_matrix, seat_w, seat_h, start_x, occupied_list, empty_list)
            roi_matrix = g.seat_collision(roi_matrix, seat_w, pimage_w, occupied_list, empty_list)

            # matrix를 숫자로 전환
            num = b.matrix_to_num(roi_matrix)
            print(num)

            # db 입력 시, 함께 저장할 좌석 line의 시작 좌표 (전체 이미지 기준)
            db_x, db_y = b.starting_point(i, roi_points, y_points[j][0])
            print("x: ", db_x, ", y: ", db_y)
            fc.write('%s %s\n' % (db_x, db_y))

            # f.write("%d %d\n" % (db_x, db_y))

            # DB에 저장된 숫자를 다시 matrix 형으로 반환
            new_matrix = b.num_to_matrix(num, roi_matrix)
            print(roi_matrix)
            fc.write('%s\n' % ' '.join([str(x) for x in roi_matrix]))
            for mat in roi_matrix:
                f.write("%d " % mat)
                if mat != 0:
                    totalSeatNum += 1
                    if mat == 1:
                        emptySeatNum += 1
            f.write("\n")

            seats.append({"x": db_x, "y": db_y, "list": roi_matrix})
            # print("new ", new_matrix)
            # key = cv2.waitKey(0)

    fc.close()
    # json_convert함수에 dictionary 넘겨줌

    imageGen()

    dic_for_json["seats"] = seats
    dic_for_json["total_seats"] = totalSeatNum
    dic_for_json["empty_seats"] = emptySeatNum
    json_convert(dic_for_json)


def imageGen():
    f = open('convert.txt', 'r')
    winy, winx = map(int, f.readline().split())
    seat_w, seat_h = map(int, f.readline().split())

    image = Image.new("RGB", (winx, winy), color_rgb(0, 0, 0))
    draw = ImageDraw.Draw(image)

    for i in range(41):
        data = f.readline()
        if data.strip() == "":
            break

        x, y = map(int, data.split())
        num = f.readline().split()

        for j in num:
            if j == '0':
                colrgb = color_rgb(0, 0, 0)
            elif j == '1':
                colrgb = color_rgb(67, 65, 66)
            else:
                colrgb = color_rgb(64, 132, 34)

            draw.rectangle([(x, y), (x + seat_w, y + seat_h)], fill=colrgb)

            x = x + 3 + seat_w

    f.close()

    filename = "convert.gif"
    image.save(filename)
    image.resize((200, 150)).save("convert_thumbnail.gif")

if __name__ == "__main__":
    main()
