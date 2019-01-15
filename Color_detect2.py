# -*- coding: UTF-8 -*-

import cv2
import numpy as np

def cut_roi(image, min_y, max_y, w):
    line_roi = image[min_y:max_y, 0:w]
    #cv2.imshow("roi", line_roi)

    return line_roi

def seat_detect(thresh, w, h):
    seat_list = []

    (_, contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (200 < area <= w*h):
            x, y, w, h = cv2.boundingRect(contour)
            seat_list.append((x, y, w, h))  # 개체 리스트에 추가

    seat_list.sort()

    return seat_list

def check_seat_color(seat_roi, seat_w, seat_h):

    hsv = cv2.cvtColor(seat_roi, cv2.COLOR_BGR2HSV)

    # 각 객체의 hsv 색상 범위 설정
    # bseat: 초록 좌석, pseat: 보라 좌석, empty: 빈 좌석
    seat_lower = np.array([42, 82, 30], np.uint8)   # 기존 세븐피시방: 20, 70, 82
    seat_upper = np.array([113, 255, 255], np.uint8) # 기존 세븐피시방: 94, 246, 240

    seat = cv2.inRange(hsv, seat_lower, seat_upper)
    kernel = np.ones((5, 5), "uint8")
    seat = cv2.dilate(seat, kernel)

    (_, contours, hierarchy) = cv2.findContours(seat, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if(contours==[]):
        #print("0")
        return False
    else:
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            # 파란색 영역이 700이상일 때, 좌석이라고 간주한다
            if (area > seat_w * seat_h * 0.7):
                return True
            else:
                return False

def seat_color_detect(roi, seat_list, seat_w, seat_h):
    occupied_list = []
    empty_list = []

    for i in range(len(seat_list)):
        # 좌석 하나씩
        x, y, w, h = seat_list[i]
        seat_roi = roi[y:y+h, x:x+w]

        if(check_seat_color(seat_roi, seat_w, seat_h)):
            roi = cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
            occupied_list.append((x, y, w, h))
        else:
            roi = cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
            empty_list.append((x, y, w, h))

    #cv2.imshow("seat_roi", roi)

    #print("full:", occupied_list)
    #print("empty: ",empty_list)

    #key = cv2.waitKey(0)
    occupied_list.sort()
    empty_list.sort()

    return occupied_list, empty_list
