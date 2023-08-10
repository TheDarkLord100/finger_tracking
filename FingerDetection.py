import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Code for importing Image List
# folderPath = "Images"
# myList = os.listdir(folderPath)
# print(myList)
# overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     overlayList.append(image)
# print(len(overlayList))

cTime = 0
pTime = 0

detector = htm.handDetector()

tipIds = [8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, Hand = detector.findHands(img=img)
    lmList = detector.findPosition(img=img, draw=False)

    if Hand != "Both" and Hand != None:
        ThumbOpen = False
        if(Hand == "Right" and lmList[4][1] < lmList[3][1]):
            ThumbOpen = True
        if(Hand == "Left" and lmList[4][1] > lmList[3][1]):
            ThumbOpen = True
        if len(lmList) != 0:
            fingers = []
            if (ThumbOpen):
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(0, 4):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            print(fingers)

            # Code for overlaying corresponding image
            # totalFingers = fingers.count(1)
            # h, w, c = overlayList[totalFingers].shape
            # img[0:h, 0:w] = overlayList[totalFingers]





    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)