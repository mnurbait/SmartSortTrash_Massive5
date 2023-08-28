import os
import cvzone
from cvzone.ClassificationModule import Classifier
import cv2
import RPi.GPIO as GPIO
import time

# Inisialisasi pin servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)  # 50Hz frequency

cap = cv2.VideoCapture(0)
classifier = Classifier('Resources/Model/keras_model.h5', 'Resources/Model/labels.txt')
imgArrow = cv2.imread('Resources/arrow.png', cv2.IMREAD_UNCHANGED)
classIDBin = 0

# Import all the waste images
imgWasteList = []
pathFolderWaste = "Resources/Waste"
pathList = os.listdir(pathFolderWaste)
for path in pathList:
    imgWasteList.append(cv2.imread(os.path.join(pathFolderWaste, path), cv2.IMREAD_UNCHANGED))

# Import all the waste images
imgBinsList = []
pathFolderBins = "Resources/Bins"
pathList = os.listdir(pathFolderBins)
for path in pathList:
    imgBinsList.append(cv2.imread(os.path.join(pathFolderBins, path), cv2.IMREAD_UNCHANGED))

# 1 = ORGANIK
# 2 = PLASTIK
# 3 = B3
# 4 = LOGAM

classDic = {0: None,
            1: 1,
            2: 2,
            3: 3,
            4: 4}

while True:
    _, img = cap.read()
    imgResize = cv2.resize(img, (454, 340))

    imgBackground = cv2.imread('Resources/background.png')

    predection = classifier.getPrediction(img)

    classID = predection[1]
    print(classID)
    if classID != 0:
        imgBackground = cvzone.overlayPNG(imgBackground, imgWasteList[classID - 1], (909, 127))
        imgBackground = cvzone.overlayPNG(imgBackground, imgArrow, (978, 320))
        classIDBin = classDic[classID]

        # Menggerakan servo berdasarkan classIDBin
        if classIDBin == 1:
            # Logika untuk menggerakan servo sesuai dengan class ID 0
            servo.start(0)
            servo.ChangeDutyCycle(5)
            time.sleep(2)
            servo.ChangeDutyCycle(0)
            time.sleep(5)
            servo.ChangeDutyCycle(12.5)
            time.sleep(2)
            servo.stop ()
        if classIDBin == 2:
            # Logika untuk menggerakan servo sesuai dengan class ID 1
            servo.start(0)
            servo.ChangeDutyCycle(7.5)
            time.sleep(2)
            servo.ChangeDutyCycle(0)
            time.sleep(5)
            servo.ChangeDutyCycle(10)
            time.sleep(2)
            servo.stop ()
        if classIDBin == 3:
            # Logika untuk menggerakan servo sesuai dengan class ID 2
            servo.start(0)
            servo.ChangeDutyCycle(5)
            time.sleep(2)
            servo.ChangeDutyCycle(0)
            time.sleep(5)
            servo.ChangeDutyCycle(12.5)
            time.sleep(2)
            servo.stop ()
        if classIDBin == 4:
            # Logika untuk menggerakan servo sesuai dengan class ID 3
            servo.start(0)
            servo.ChangeDutyCycle(7.5)
            time.sleep(2)
            servo.ChangeDutyCycle(0)
            time.sleep(5)
            servo.ChangeDutyCycle(10)
            time.sleep(2)
            servo.stop ()
    imgBackground = cvzone.overlayPNG(imgBackground, imgBinsList[classIDBin], (895, 374))

    imgBackground[148:148 + 340, 159:159 + 454] = imgResize
    # Displays
    # cv2.imshow("Image", img)
    cv2.imshow("Output", imgBackground)
    cv2.waitKey(1)
