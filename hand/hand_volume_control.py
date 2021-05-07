import numpy as np
import time
import cv2
import hand_tracking_module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# variables
cTime = 0
pTime = 0
imw = 700
imh = 480
length = 0
vol = 0
volPer = 0
volBar = 395
lmList = []
detector = htm.handDetector(detectionCon=0.8)

################################################

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


################################################

# cap = cv2.VideoCapture('video/volume2.mp4')
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.resize(img, (imw,imh))
    img = detector.findHands(img)

    lmList = detector.handPosition(img,draw = False)

    # Volume Bar

    cv2.rectangle(img,(550,400),(600,150),(255,0,0),2)
    cv2.rectangle(img,(555,395),(595,int(volBar)),(255,0,0),cv2.FILLED)
    cv2.putText(img, f'{(int(volPer))}%',(545,140), cv2.FONT_HERSHEY_TRIPLEX,0.7,
                (255,0,0),1)
    
    ################################################

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
        cv2.circle(img, (cx,cy),10,(0,0,255),cv2.FILLED)
        cv2.circle(img, (x1,y1),7,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2,y2),7,(255,0,0),cv2.FILLED)


        length = np.hypot(x2-x1, y2-y1)
        if (length<=50):
            cv2.circle(img, (cx,cy),10,(0,255,0),cv2.FILLED)
            

        # Hand Range 50 - 150
        vol = np.interp(length, (50,150), (minVol, maxVol))
        volBar = np.interp(length, (50,150), (395,155))
        volPer = np.interp(length, (50,150), (0,100))
        # volume.SetMasterVolumeLevel(vol, None)

        

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'fps:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()