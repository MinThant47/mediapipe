import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon = 0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img    

    def handPosition(self, img, handNo = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for index,lm in enumerate(myHand.landmark):
                h, w , c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([index, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255,255,0), cv2.FILLED)

        return lmList
              


def main():
    cTime = 0
    pTime = 0
    lmList = []
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        ret, img = cap.read()
        cTime = time.time()
        img = detector.findHands(img)
        lmList = detector.handPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255), 3)
        cv2.imshow('video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()