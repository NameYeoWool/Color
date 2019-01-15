# -*- coding: UTF-8 -*-
################################
################################
# 모듈명    : gui.py
# 작성자    : 서혜리
# 설명      : 캡쳐할 화면의 좌표값을 저장하고 이를 기준으로 캡쳐한 후 main함수를 실행시키는 gui 프로그램
#
#             pyinstaller 라이브러리를 사용하여 실행파일로 만듦 -> 터미널에서 pyinstaller --onefile --noconsole "gui.py" -> dist폴더에 저장됨
#             --onefile: 하나의 파일로 만들기(실행시간이 느려지는 단점이 있음
#             --noconsole: 콘솔창을 띄우지 않음 (띄워주는게 디폴트)
#             참고 블로그: https://m.blog.naver.com/mandori21/220372958993
################################
################################

from pynput import mouse  # 키보드, 마우스 i/o
import tkinter as tk  # gui
from PIL import ImageTk, Image
from PIL import ImageGrab  # 이미지 캡쳐
from Main import main
import time  # 파이썬 기본라이브러리
import json
import logging
from graphics import *
from random import *
from PIL import Image, ImageDraw

# tkinter root 윈도우 생성

root = tk.Toplevel()
root.resizable(False, False)
root.title("Watcher Daemon")
root.geometry("400x400+0+0")

thumbnailLbl = None
thumbnailLbl2 = None

# 전역변수 선언

start_point = ()  # 캡쳐 화면 시작점
end_point = ()  # 캡쳐 화면 끝점
take_shot = False  # start, stop버튼 flag


################################
# 함수명    : point
# 작성자    : 서혜리
# 설명      : 해당 키보드 버튼을 누르면 마우스 좌표를 읽어와 저장한다
# 리턴      : _
# 매개변수  : tkinter의 event 리스너로부터 받은 event (키보드 버튼 클릭)
################################

def point(event):
    print(event.char)
    if event.char == 's':
        global start_point
        start_point = mouse.Controller().position  # 현재의 마우스 위치를 시작포인트로 지정
        startLbl.config(text=mouse.Controller().position)  # label 바꿔줌
    if event.char == 'e':
        global end_point
        end_point = mouse.Controller().position  # 현재의 마우스 위치를 끝포인트로 지정
        endLbl.config(text=mouse.Controller().position)  # 라벨 바꿔줌


################################
# 함수명    : screenshot
# 작성자    : 서혜리
# 설명      : 저장된 좌표(전역변수)를 이용해 10초 간격으로 스크린샷을 캡쳐 후 저장한다.
# 리턴      : _
# 매개변수  : -
################################

def screenshot():
    if not take_shot:  # 정지 버튼을 눌렀을 때
        return

    try:
        imgGrab = ImageGrab.grab(bbox=(*start_point, *end_point))  # 이미지 캡쳐
        imgGrab.save("screen_shot.png")
        imgGrab.resize((200, 150)).save("thumbnail.gif")

        # if thumbnailLbl:
        #    thumbnailLbl.destroy()
        thumbnailImg = tk.PhotoImage(file="thumbnail.gif")
        thumbnailLbl = tk.Label(canvas, image=thumbnailImg)
        thumbnailLbl.image = thumbnailImg
        thumbnailLbl.place(x=0, y=0)

        # try:
        main()
        # except Exception:
        #     logging.error("unexpected error in main function")

        # if thumbnailLbl2:
        #    thumbnailLbl2.destroy()
        thumbnailImg2 = tk.PhotoImage(file="convert_thumbnail.gif")
        thumbnailLbl2 = tk.Label(canvas, image=thumbnailImg2)
        thumbnailLbl.image2 = thumbnailImg2
        thumbnailLbl2.place(x=200, y=0)
        print("o")

        fo = open("pc_info.json")
        json_info = json.load(fo)
        fo.close()

        if json_info["empty_seats"] == 0:
            logging.warning("no seats detected")
        else:
            logging.info("json file generated")

        emptySeatsLbl.config(text="빈 좌석:" + str(json_info["empty_seats"]))
    except:
        pass

    root.after(20000, screenshot)


################################
# 함수명    : start
# 작성자    : 서혜리
# 설명      : tkinter gui의 시작 버튼을 누르면 flag를 true로 바꾼 후 label을 바꿔주고 screenshot함수를 호출한다
# 리턴      : _
# 매개변수  : -
################################

def start():
    if start_point == () or end_point == ():
        return;
    global take_shot
    take_shot = True
    processLbl.config(text="시작")
    time.sleep(5)
    screenshot()


################################
# 함수명    : stop
# 작성자    : 서혜리
# 설명      : tkinter gui의 멈춤 버튼을 누르면 flag를 false로 바꿔준다
# 리턴      : _
# 매개변수  : -
################################

def stop():
    global take_shot
    take_shot = False
    processLbl.config(text="멈춤")



# image_canvas = tk.Canvas(root)  # root 창 안에 canvas를 하나 더 생성해줌
# image_canvas.pack()

canvas = tk.Canvas(root)  # root 창 안에 canvas를 하나 더 생성해줌
canvas.place(x=0, y=0, width=400, height=640)
canvas.bind('<Key>', point)  # key보드와 point함수를 bind해줌
canvas.focus_set()  # canvas를 활성화 시켜줌

info_canvas = tk.Canvas(root)
info_canvas.place(x=0, y=200, width=400, height=440)

emptySeatsLbl = tk.Label(info_canvas, text="빈 좌석:0")
emptySeatsLbl.pack()

lbl0 = tk.Label(info_canvas, text="시작 좌표 -> press s")
lbl0.pack()

startLbl = tk.Label(info_canvas, text=" START")
startLbl.pack()

lbl1 = tk.Label(info_canvas, text="끝 좌표 -> press e")
lbl1.pack()

endLbl = tk.Label(info_canvas, text=" END")
endLbl.pack()

processLbl = tk.Label(info_canvas, text="멈춤")
processLbl.pack()

start_btn = tk.Button(info_canvas, text="START", width=15, command=start)
start_btn.pack()

end_btn = tk.Button(info_canvas, text="END", width=15, command=stop)
end_btn.pack()

root.mainloop()
