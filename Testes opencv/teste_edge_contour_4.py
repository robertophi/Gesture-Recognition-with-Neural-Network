import cv2
import numpy as np
import time

# Open Camera object
cap = cv2.VideoCapture(0)



def nothing(x):
    pass


def filterLines(lines):
    a, b, c = lines.shape
    filtered_lines = []
    for i in range(a):
        xi = lines[i][0][0]
        xf = lines[i][0][2]
        yi = lines[i][0][1]
        yf = lines[i][0][3]
        dx = xi-xf
        dy = yi-yf
        size = dx**2+dy**2
        print(size)
        if size > 5000:
            filtered_lines.append(((xi,yi),(xf,yf)))
    return filtered_lines

# Creating a window for HSV track bars
cv2.namedWindow('HSV_TrackBar')



# Creating track bar
cv2.createTrackbar('up', 'HSV_TrackBar', 180, 255, nothing)
cv2.createTrackbar('lower', 'HSV_TrackBar', 80, 255, nothing)

kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


while (1):

    upper = cv2.getTrackbarPos('up', 'HSV_TrackBar')
    lower = cv2.getTrackbarPos('lower', 'HSV_TrackBar')
    # Measure execution time

    # Capture frames from the camera
    ret, originalFrame = cap.read()

    frame = originalFrame[:, 0:300]




    originalGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(originalGray, (3, 3), 0)
    gray = cv2.dilate(gray, kernel_ellipse, iterations=1)
    gray = cv2.equalizeHist(gray)


    #Original edges = apenas o edge obtido da imagem atual
    #Simple edge = edge da imagem atual processado
    #Previous edges = edges calculados das imagem anteriores

    originalEdges = cv2.Canny(gray, lower, upper)
    edges_simple = originalEdges
    edges_simple[-120:, :] = 0
    edges_simple = cv2.dilate(edges_simple, kernel_ellipse, iterations=4)
    edges_simple = cv2.erode(edges_simple, kernel_ellipse, iterations=2)

    try:
        edges = cv2.bitwise_or(edges_simple,prev1_edges)
        edges = cv2.bitwise_or(edges,prev2_edges)
    except:
        edges = edges_simple
        print("No previous edge")

    prev1_edges = edges_simple
    prev2_edges = prev1_edges

    edges = cv2.dilate(edges, kernel_ellipse,iterations=1)
    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    try:
        minLineLength = 80
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 100, threshold=80, lines=np.array([]),
                                minLineLength=minLineLength, maxLineGap=20)

        filtered_lines = filterLines(lines)
        for line in filtered_lines:
            cv2.line(gray, line[1] , line[0], (0, 0, 255), 3, cv2.LINE_AA)

    except:
        print("Line problem")
    maxArea = 0
    for cnt in contours:
        newArea = cv2.contourArea(cnt)
        if newArea > maxArea:
            maxArea = newArea
            biggestContour = cnt

    try:
        #cv2.drawContours(originalFrame, biggestContour, -1, (0, 255, 0), 3,2)
        hull = cv2.convexHull(biggestContour, returnPoints=False)
        defects = cv2.convexityDefects(biggestContour, hull)
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if (d > 0):
                start = tuple(biggestContour[s][0])
                end = tuple(biggestContour[e][0])
                far = tuple(biggestContour[f][0])
                cv2.line(originalFrame, start, end, [0, 255, 0], 2)
                midx = int((start[0] + end[0]) / 2)
                midy = int((start[1] + end[1]) / 2)
                midpoint = (midx, midy)
                cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
                cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)


    except:
        print("No contour found")

    cv2.imshow("Edges", edges)
    cv2.imshow("Gray", gray)
    cv2.imshow("Frame", originalFrame)
    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
