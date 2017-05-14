import numpy as np
from collections import defaultdict
from PyQt5.QtCore import QThread
<<<<<<< HEAD
import cv2, time, math
=======
import cv2, time
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f


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


<<<<<<< HEAD
def angle(biggestContour):
    angle_p = 0
    angle_acum = 0
    for i in range(biggestContour.shape[0]-1):
        dx = biggestContour[i][0][0]-biggestContour[i+1][0][0]
        dy = biggestContour[i][0][1]-biggestContour[i+1][0][1]
        try:
            angle = math.atan(dy/dx)
        except:
            angle = 1.57
        angle_change = abs(angle_p-angle)
        angle_acum += angle_change
        angle_p = angle
    print(angle_acum)

def filterHullDefects( defects):
    defects_index_list = []
    defects_list = []
    max = 0
    max_index = -1
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        if (d > 4000):
            if d>max:
                max = d
                max_index = i
            defects_index_list.append(i)
    defects_index_list.remove(max_index)
    for j in defects_index_list:
        s,e,f,d = defects[j,0]
        defects_list.append([s,e,f,d])
    return defects_list

=======
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f
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
<<<<<<< HEAD
cap = cv2.VideoCapture('output3.avi')
=======
cap = cv2.VideoCapture('output.avi')
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f

kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while (running and cap.isOpened()):
<<<<<<< HEAD
    time.sleep(0.0566)
=======
    time.sleep(0.03666)
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f
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
<<<<<<< HEAD
        defects_list = filterHullDefects(defects)
        for s, e, f, d in defects_list:
            start = tuple(biggestContour[s][0])
            end = tuple(biggestContour[e][0])
            far = tuple(biggestContour[f][0])
            midx = int((start[0] + end[0]) / 2)
            midy = int((start[1] + end[1]) / 2)
            midpoint = (midx, midy)
            cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
            cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)
=======
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if (d > 0):
                start = tuple(biggestContour[s][0])
                end = tuple(biggestContour[e][0])
<<<<<<< HEAD
                cv2.line(originalFrame, start, end, [0, 255, 0], 2)

=======
                far = tuple(biggestContour[f][0])
                cv2.line(originalFrame, start, end, [0, 255, 0], 2)
                midx = int((start[0] + end[0]) / 2)
                midy = int((start[1] + end[1]) / 2)
                midpoint = (midx, midy)
                cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
                cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)
        attr_dict=cnt_hull_attributes(biggestContour)
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f

    except:
        print("No contour found")
        ##########################################

<<<<<<< HEAD

    '''
    try:
        epsilon = 1
        approx = cv2.approxPolyDP(biggestContour, epsilon, True)
        cv2.polylines(originalFrame, approx, True, (0,0,255),4,lineType=cv2.LINE_AA)
        angle(approx)
        print("\n")
    except:
        print("No polygon")
    '''


=======
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f
    if (visibleFrame == True):
        cv2.imshow("Frame", originalFrame)
    if (visibleEdges == True):
        cv2.imshow("Edges", edges)
    if (visibleGray == True):
        cv2.imshow("Gray", gray)
    # close the output video by pressing 'ESC'
<<<<<<< HEAD
    k = cv2.waitKey(1) & 0xFF
=======
    k = cv2.waitKey(5) & 0xFF
>>>>>>> be118b9fae6c53433a4f2c6c1bb1436d6edf0d0f
    if k == 27:
        running = False
        break

cap.release()
cv2.destroyAllWindows()


