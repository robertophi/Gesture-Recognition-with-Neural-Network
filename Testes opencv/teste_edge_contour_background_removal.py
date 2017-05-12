import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(0)

# Decrease frame size


def nothing(x):
    pass



# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')

# Starting with 100's to prevent error while masking
h, s, v = 100, 100, 100


# Creating track bar
cv2.createTrackbar('up', 'HSV_TrackBar', 180, 255, nothing)
cv2.createTrackbar('lower', 'HSV_TrackBar', 130, 255, nothing)

kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


fgbg = cv2.createBackgroundSubtractorMOG2(history=100)
while (1):

    upper = cv2.getTrackbarPos('up','HSV_TrackBar')
    lower = cv2.getTrackbarPos('lower','HSV_TrackBar')

    print((upper,lower))
    # Measure execution time

    # Capture frames from the camera
    ret, frame = cap.read()

    # Blur the image
    frame = cv2.blur(frame, (3, 3))
    frame = cv2.medianBlur(frame,5)


    #escolhendo apenas a parte da esquerda da imagem
    #retirando o background
    fgmask = fgbg.apply(frame)
    fgmask[:,320:] = 0

    mask_eroded = cv2.erode(fgmask,kernel_ellipse,iterations=1)
    mask_dilated = cv2.dilate(mask_eroded,kernel_ellipse,iterations=3)

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    gray = cv2.dilate(gray,kernel_ellipse, iterations=3)


    edges = cv2.Canny(gray, lower, upper)
    edges = cv2.dilate(edges,kernel_ellipse, iterations=1)

    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maxArea = 0
    for cnt in contours:
        newArea = cv2.contourArea(cnt)
        if newArea > maxArea:
            maxArea =  newArea
            biggestContour = cnt

    try:
        cv2.drawContours(frame, biggestContour, -1, (0, 255, 0), 3)

        #epsilon = 0.1 * cv2.arcLength(cnt, True)
        #approx = cv2.approxPolyDP(biggestContour, epsilon, True)
        #cv2.drawContours(frame, [approx], -1, (0, 0, 255), 3)

    except:
        print("No contour found")

    # Draw Contours
    #cv2.drawContours(frame, contours, -1, (122,122,0), 3)
    cv2.imshow("edge", edges)
    cv2.imshow("Gray",gray)
    cv2.imshow("Frame",frame)

    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()