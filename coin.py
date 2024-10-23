import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder
import pyttsx3
from tkinter import *
import threading
import subprocess
import time



def cam():

    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)

    totalMoney = 0

    myColorFinder = ColorFinder(False)
    # Custom Orange Color
    hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 145, 'hmax': 63, 'smax': 91, 'vmax': 255}

    def speak(audio):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voices',voices[0].id)
        engine.say(audio)
        engine.runAndWait()


    def empty(a):
        pass


    cv2.namedWindow("Settings")
    cv2.resizeWindow("Settings", 640, 240)
    cv2.createTrackbar("Threshold1", "Settings", 70, 255, empty)
    cv2.createTrackbar("Threshold2", "Settings", 226, 255, empty)
    cv2.createTrackbar("area", "Settings", 400,1000, empty)

    def preProcessing(img):
        imgPre = cv2.GaussianBlur(img, (5, 5), 3)
        thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
        thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
        imgPre = cv2.Canny(imgPre, thresh1, thresh2)
        kernel = np.ones((3, 3), np.uint8)
        imgPre = cv2.dilate(imgPre, kernel, iterations=2)
        imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)

        return imgPre


    while True:
        success, img = cap.read()
        imgPre = preProcessing(img)
        minArea = cv2.getTrackbarPos("area", "Settings")
        imgContours, conFound = cvzone.findContours(img, imgPre, minArea)


        totalMoney = 0
        imgCount = np.zeros((480, 640, 3), np.uint8)

        if conFound:
            for count, contour in enumerate(conFound):
                peri = cv2.arcLength(contour['cnt'], True)
                approx = cv2.approxPolyDP(contour['cnt'], 0.02 * peri, True)

                if len(approx) > 5:
                    area = contour['area']
                    x, y, w, h = contour['bbox']
                    imgCrop = img[y:y + h, x:x + w]
                    # cv2.imshow(str(count),imgCrop)
                    imgColor, mask = myColorFinder.update(imgCrop, hsvVals)
                    whitePixelCount = cv2.countNonZero(mask)
                    # print(whitePixelCount)

                    if area < 6500:
                        totalMoney += 1
                    elif 6500 < area < 8500:
                        totalMoney += 2
                    elif area > 8500:
                        totalMoney += 10


        # print(totalMoney)
        cvzone.putTextRect(imgCount, f'Rs.{totalMoney}', (100, 200),scale=10,offset=30,thickness=7)

        imgStacked = cvzone.stackImages([img, imgPre, imgContours,imgCount], 2, 0.7)
        cvzone.putTextRect(imgStacked, f'Rs.{totalMoney}', (50, 50))


        cv2.imshow("Image", imgStacked)
        #speak(totalMoney)
        # cv2.imshow("imgColor", imgColor)
        cv2.waitKey(1)




def background(start):
        threading.Thread(target=start).start()





def gui():
    root = Tk()
    root.configure(background="black")
    root.title("AI Coin Counter")
    root.wm_iconbitmap("download.svg")
   # root.attributes("-fullscreen",True)
    root.geometry("800x800")
    title = Label(text="WELCOME",bg="black",fg="white",padx="40",font="Helvetica 29 bold")

    f1 = Frame(root,borderwidth=0,bg="black",relief=SUNKEN)
    f1.pack(padx=0.5,pady=0.5)

    f2 = Frame(root,borderwidth=0,bg="black",relief=SUNKEN)
    f2.pack(padx=0.5,pady=0.5)

    b1=Button(f1,fg="white",text="START",bg="black",bd="0",font="lucida 12 bold",command=lambda:background(start))
    b1.pack(padx=30,pady=50)


    b3=Button(f1,fg="white",text="EXIT",bg="black",bd="0",font="lucida 12 bold",command=exit)
    b3.pack(padx=90,pady=100)

    title.pack()

    frameCnt = 20
    frames = [PhotoImage(file="jarvis-iron-man.gif",format = 'gif -index %i' %(i)) for i in range(frameCnt)]

    def update(ind):

        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label.configure(image=frame)
        root.after(100, update, ind)
    label = Label(f2,bd=0,highlightthickness=0)
    label.pack()
    root.after(0, update, 0)

    root.mainloop()


def start():
    cam()


if __name__ == "__main__":

    print("going..")
    #gui()
    start()
