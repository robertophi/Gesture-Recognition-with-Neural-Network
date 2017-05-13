import numpy as np
from collections import defaultdict
from PyQt5.QtCore import QThread
import cv2, time


def filterLines(lines):
    a, b, c = lines.shape
    filtered_lines = []
    for i in range(a):
        xi = lines[i][0][0]
        xf = lines[i][0][2]
        yi = lines[i][0][1]
        yf = lines[i][0][3]
        dx = xi - xf
        dy = yi - yf
        size = dx ** 2 + dy ** 2
        if size > 5000 and size < 25000:
            filtered_lines.append(((xi, yi), (xf, yf)))
    return filtered_lines


def dictLines(lines):
    lines_dict = {}
    for line in lines:
        rho = line[0][0]
        theta = line[0][1]
        theta_d = int(theta * 180 / np.pi)
        try:
            lines_dict[theta_d] += 1
        except:
            lines_dict[theta_d] = 1
    return lines_dict


# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_properties/py_contour_properties.html
def cnt_hull_attributes(contour):
    hull = cv2.convexHull(contour)
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    extent = area / (w * h)
    moment = cv2.moments(contour)
    attr_dict = {"area" : area,
            "perimeter": perimeter,
            "solitidy":solidity,
            "aspect_ratio":aspect_ratio,
            "extent":extent}
    for i in moment.keys():
        if i[0] == "n":
            attr_dict[i] = moment[i]
    return attr_dict


upper = 200
lower = 80
thresh = 100
minLineSize = 30

visibleFrame = True
visibleEdges = True
visibleGray = True

running = False

running = True

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('output.avi')

kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while (running and cap.isOpened()):
    time.sleep(0.03666)
    # Capture frames from the camera
    ret, originalFrame = cap.read()
    if ret == False:
        print("Erro na leitura da câmera")
        running = False
        break
    frame = originalFrame[:, 0:300]

    ##########################################
    originalGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(originalGray, (3, 3), 0)
    gray = cv2.dilate(gray, kernel_ellipse, iterations=1)
    gray = cv2.equalizeHist(gray)
    ##########################################




    ##########################################
    # Original edges = apenas o edge obtido da imagem atual
    # Simple edge = edge da imagem atual processado
    # Previous edges = edges calculados das imagem anteriores

    originalEdges = cv2.Canny(gray, lower, upper)
    edges_simple = originalEdges
    edges_simple[-120:, :] = 0
    edges_simple = cv2.dilate(edges_simple, kernel_ellipse, iterations=4)
    edges_simple = cv2.erode(edges_simple, kernel_ellipse, iterations=2)

    try:
        edges = cv2.bitwise_or(edges_simple, prev1_edges)
        edges = cv2.bitwise_or(edges, prev2_edges)
    except:
        edges = edges_simple

    prev1_edges = edges_simple
    prev2_edges = prev1_edges

    edges = cv2.dilate(edges, kernel_ellipse, iterations=2)
    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ##########################################





    ##########################################
    try:
        lines = cv2.HoughLines(image=edges, rho=10,
                               theta=np.pi / 6, threshold=30)
        lines_dict = dictLines(lines)
    except:
        print("Standard Hough Line problem")
        ##########################################





        ##########################################
    try:
        lines_p = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 100,
                                  threshold=thresh, lines=np.array([]),
                                  minLineLength=minLineSize, maxLineGap=20)

        filtered_lines = filterLines(lines_p)
        for line in filtered_lines:
            cv2.line(gray, line[1], line[0], (0, 0, 255), 3, cv2.LINE_AA)
    except:
        print("Probabilistic Line problem")
        ##########################################





        ##########################################
    maxArea = 0
    for cnt in contours:
        newArea = cv2.contourArea(cnt)
        if newArea > maxArea:
            maxArea = newArea
            biggestContour = cnt

    try:
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
        attr_dict=cnt_hull_attributes(biggestContour)

    except:
        print("No contour found")
        ##########################################

    if (visibleFrame == True):
        cv2.imshow("Frame", originalFrame)
    if (visibleEdges == True):
        cv2.imshow("Edges", edges)
    if (visibleGray == True):
        cv2.imshow("Gray", gray)
    # close the output video by pressing 'ESC'
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        running = False
        break

cap.release()
cv2.destroyAllWindows()


