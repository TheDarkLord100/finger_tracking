import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "Images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

cTime = 0
pTime = 0

detector = htm.handDetector()

tipIds = [8, 12, 16, 20]

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

while True:
    success, img = cap.read()
    img = detector.findHands(img=img)
    lmList = detector.findPosition(img=img, draw=False)

    if len(lmList) != 0:
        fingers = []
        if (lmList[4][1] < lmList[3][1]):
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(0, 4):
            # print(lmList[4][1])
            # print(lmList[2][1])
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        print(fingers)
        totalFingers = fingers.count(1)

        h, w, c = overlayList[totalFingers].shape
        img[0:h, 0:w] = overlayList[totalFingers]





    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)