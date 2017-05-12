import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(0)


def findHandColor(cap):
    start = time.time()
    color = []
    while(time.time()-start < 3):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        centerx = 500
        centery = 300

        cv2.circle(frame, (centerx, centery), 30, (255, 120, 120), 3)
        window = hsv[centery - 50:centery + 50, centerx - 50:centerx + 50]
        mean = cv2.mean(window)
        color.append(mean[0])


        cv2.imshow("Frame", frame)
        cv2.waitKey(5)
    cv2.destroyAllWindows()
    return sum(color[-10:])/10


handColor = findHandColor(cap)
while(1):

    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([handColor-10, 0, 0]), np.array([handColor+10, 255, 255]))
    cv2.imshow("Hand color mask", mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()