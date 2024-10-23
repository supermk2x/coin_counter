import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

totalMoney = 0

myColorFinder = ColorFinder(False)
# Custom Orange Color
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 145, 'hmax': 63, 'smax': 91, 'vmax': 255}



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
                print(area)

    imgStacked = cvzone.stackImages([img, imgPre, imgContours,imgCount], 2, 0.5)
    cvzone.putTextRect(imgStacked, f'Rs.{totalMoney}', (50, 50))

    cv2.imshow("Image", imgStacked)
    # cv2.imshow("imgColor", imgColor)
    cv2.waitKey(1)
