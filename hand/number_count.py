import cv2
import time
import hand_tracking_module as htm

# variable
cTime = 0
pTime = 0
lmList = []

tipid = [4,8,12,16,20]
detector = htm.handDetector(detectionCon=0.5)

cap = cv2.VideoCapture('video/count.mp4')
# cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.resize(img, (700, 480))

    detector.findHands(img)
    lmList = detector.handPosition(img, draw = False)

    if len(lmList) != 0:
        finger = []
        if lmList[tipid[0]][1] > lmList[tipid[0]-1][1] :
            finger.append(1)
        else:
            finger.append(0)

        for index in range(1,5):
            if lmList[tipid[index]][2] < lmList[tipid[index]-2][2]:
                finger.append(1)
            else:
                finger.append(0)

        print(finger.count(1))
        cv2.rectangle(img, (510,150), (610,300), (255,0,0), cv2.FILLED)
        cv2.putText(img, f'{finger.count(1)}', (530,250), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)   
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'fps: {int(fps)}', (40,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255))
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()