import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

fps = 0
while (1):
    t=  time.time()


    # Capture frames from the camera
    ret, frame = cap.read()
    fps_c = 1 / (time.time() - t)
    fps = 0.75 * fps + 0.25 * fps_c
    cv2.putText(frame, str(fps), (590, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Frame",frame)

    # close the output video by pressing 'ESC'
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()