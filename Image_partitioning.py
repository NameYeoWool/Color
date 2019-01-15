# -*- coding: UTF-8 -*-

def set_roi(image, min, max):
    roi = image[min[1]:max[1], min[0]:max[0]]
    #cv2.imshow("roi", line_roi)
    return roi

def image_partition(image, blanks_w, blanks_h):
    image_h, image_w = image.shape[:2]

    # x, y 좌표만 남게 리스트 재배열
    w_points = []
    for i in range(len(blanks_w)):
        if(i==0):
            if(blanks_w[0][1]!=0):
                w_points.append(0)

        if(blanks_w[i][1] == 0):
            if(blanks_w[i][2] != image_w -1):
                w_points.append(blanks_w[i][2])
        else:
            w_points.append(blanks_w[i][1])
            if (blanks_w[i][2] != image_w - 1):
                w_points.append(blanks_w[i][2])

    h_points = []
    for i in range(len(blanks_h)):
        if (i == 0):
            if (blanks_h[0][1] != 0):
                h_points.append(0)

        if (blanks_h[i][1] == 0):
            if (blanks_h[i][2] != image_h - 1):
                h_points.append(blanks_h[i][2])
        else:
            h_points.append(blanks_h[i][1])
            if (blanks_h[i][2] != image_h - 1):
                h_points.append(blanks_h[i][2])

    # 재배열한 리스트를 바탕으로 분할 이미지마다의 좌표 구하기
    img_points = []
    for i in range(len(w_points)):
        for j in range(len(h_points)):
            img_points.append((w_points[i], h_points[j]))


    # y 좌표 같은 것 순으로 sort
    def takeSecond(elem):
        return elem[1]

    img_points.sort(key=takeSecond)

    # 각 영역별 이미지 대각선 꼭지점만 남기기-1.y좌표로 리스트 구분하기
    img = []
    tmp=[]
    num = img_points[0][1]
    for i in range(len(img_points)):
        if(img_points[i][1] == num):
            tmp.append(img_points[i])

            if(i==len(img_points)-1):
                img.append(tmp)
        else:
            img.append(tmp)
            num = img_points[i][1]
            tmp=[]
            tmp.append(img_points[i])

    #2. 구분된 리스트에서 이미지의 대각선 꼭지점 좌표값만 추출
    points = []
    for i in range(int(len(img)/2)):
        for j in range(len(img[0])):
            if(j%2==0):
                p1 = img[i*2][j]
                points.append(p1)
            else:
                p2 = img[i*2+1][j]
                points.append(p2)

    return points