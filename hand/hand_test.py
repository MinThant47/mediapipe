import time
import mediapipe as mp
import cv2
import hand_tracking_module as htm

cTime = 0
pTime = 0
lmList = []
cap = cv2.VideoCapture('./video/test4.mp4')
detector = htm.handDetector()

while True:
    ret, img = cap.read()
    cTime = time.time()
    img = detector.findHands(img)
    lmList = detector.handPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList)
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255), 3)
    cv2.imshow('video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()