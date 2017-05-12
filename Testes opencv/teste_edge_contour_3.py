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
cv2.createTrackbar('lower', 'HSV_TrackBar', 80, 255, nothing)

kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

fgbg = cv2.createBackgroundSubtractorMOG2(history=600)


while (1):

    upper = cv2.getTrackbarPos('up','HSV_TrackBar')
    lower = cv2.getTrackbarPos('lower','HSV_TrackBar')
    # Measure execution time

    # Capture frames from the camera
    ret, frame = cap.read()

    # Blur the image
    frame = cv2.blur(frame, (3, 3))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([2, 50, 50]), np.array([h+10, 255, 255]))
    mask = cv2.bitwise_not(mask)
    mask = cv2.erode(mask, kernel_ellipse,iterations=1)
    mask = cv2.dilate(mask, kernel_ellipse, iterations=3)
    mask = cv2.erode(mask, kernel_ellipse, iterations=2)
    mask = cv2.dilate(mask, kernel_ellipse,iterations=3)

    fgmask = fgbg.apply(frame)
    fgmask = cv2.erode(fgmask, kernel_ellipse, iterations=1)
    fgmask = cv2.dilate(fgmask, kernel_ellipse,iterations=3)
    fgmask = cv2.erode(fgmask, kernel_ellipse, iterations=1)


    maskand = cv2.bitwise_and(fgmask,mask)
    maskand[:, 280:] = 0
    maskand[-120:, :] = 0

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    gray = cv2.dilate(gray,kernel_ellipse, iterations=3)


    edges = cv2.Canny(gray, lower, upper)
    edges = cv2.dilate(edges,kernel_ellipse, iterations=4)
    edges = cv2.erode(edges,kernel_ellipse,iterations=1)

    edges[:,280:]=0
    edges[-120:,:] = 0

    masktotal = cv2.bitwise_or(edges,maskand)

    im2, contours, hierarchy = cv2.findContours(masktotal, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    maxArea = 0
    for cnt in contours:
        newArea = cv2.contourArea(cnt)
        if newArea > maxArea:
            maxArea =  newArea
            biggestContour = cnt

    try:
        #cv2.drawContours(frame, biggestContour, -1, (0, 255, 0), 3,2)
        hull = cv2.convexHull(biggestContour, returnPoints=False)
        defects = cv2.convexityDefects(biggestContour, hull)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if(d>3000):
                start = tuple(biggestContour[s][0])
                end = tuple(biggestContour[e][0])
                far = tuple(biggestContour[f][0])
                cv2.line(frame, start, end, [0, 255, 0], 2)
                midx = int((start[0]+end[0])/2)
                midy = int((start[1] + end[1]) / 2)
                midpoint = (midx,midy)
                cv2.line(frame,midpoint,far,[0,255,125],2)
                cv2.circle(frame, far, 5, [0, 0, 255], -1)


    except:
        print("No contour found")


    cv2.imshow("edge", edges)
    cv2.imshow("Frame",frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Mask fg", fgmask)
    cv2.imshow("total mask", masktotal)
    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()