import sys
import numpy as np
from collections import defaultdict
from PyQt5.QtCore import QThread
import cv2, time, math
import dataframe


class ImageProcesser(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.upper = 200
        self.lower = 80
        self.thresh = 100
        self.minLineSize = 30
        self.defectsSize = 2500

        self.bottonLine = -120
        self.visibleFrame = True
        self.visibleEdges = True
        self.visibleGray = False
        self.visibleFloodfill = True
        self.showConvexHull = True
        self.showHullDefects = True
        self.showHoughLines = True

        self.dataframe = dataframe.DataFrame()
        self.fps = 0
        self.running = False
        self.destroyAllWindows = False

    def __del__(self):
        self.wait()

    def run(self):
        self.running = True

        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture('output.avi')

        kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel_ellipse=cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        font = cv2.FONT_HERSHEY_SIMPLEX
        prev_edges = -1
        prev_flooded_edges = -1

        while (self.running and cap.isOpened()):
            if (self.destroyAllWindows == True):
                cv2.destroyAllWindows()
                self.destroyAllWindows = False
            t = time.time()
            time.sleep(0.03066)
            # Capture frames from the camera
            ret, originalFrame = cap.read()
            if ret == False:
                print("Erro na leitura da câmera")
                self.running = False
                break
            frame = originalFrame[:, 0:300]

            ##########################################
            originalGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            gray = cv2.GaussianBlur(originalGray, (5, 5), 0)
            gray = cv2.dilate(gray, kernel_ellipse, iterations=1)
            gray = cv2.equalizeHist(gray)
            gray = cv2.medianBlur(gray, 3)
            ##########################################




            ##########################################
            # Original edges = apenas o edge obtido da imagem atual
            # Simple edge = edge da imagem atual processado
            # Previous edges = edges calculados das imagem anteriores

            edges, prev_edges = self.findEdges(gray, prev_edges, kernel_ellipse)
            flooded_eges, prev_flooded_edges = self.floodFillEdges(edges, prev_flooded_edges)

            im2, contours, hierarchy = cv2.findContours(flooded_eges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ##########################################





            ##########################################
            try:
                eroded_edges = cv2.erode(flooded_eges, kernel_ellipse, iterations=2)
                lines = cv2.HoughLines(image=eroded_edges, rho=20,
                                       theta=np.pi / 6, threshold=80)
                '''for x in range(0,len(lines)):
                    for rho, theta in lines[x]:
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x0 = a * rho
                        y0 = b * rho
                        x1 = int(x0 + 1000 * (-b))
                        y1 = int(y0 + 1000 * (a))
                        x2 = int(x0 - 1000 * (-b))
                        y2 = int(y0 - 1000 * (a))

                        cv2.line(originalFrame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                '''
                lines_dict = self.dictLines(lines)
            except:
                print("Standard Hough Line problem")
                ##########################################





                ##########################################
            try:
                lines_p = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 100,
                                          threshold=self.thresh, lines=np.array([]),
                                          minLineLength=self.minLineSize, maxLineGap=20)
                filtered_lines = self.filterLines(lines_p)
            except:
                print("Probabilistic Line problem")
                ###########################################

            try:
                biggestContour = self.findContour(contours)
            except:
                print("Error na análise do contour")

            try:
                cv2.drawContours(originalFrame, [biggestContour], -1, (255, 0, 0), 2)
                hull = cv2.convexHull(biggestContour, returnPoints=False)
                defects = cv2.convexityDefects(biggestContour, hull)
                defects_list = self.filterHullDefects(defects)
                numberOfDefects = len(defects_list)
            except:
                print("No contour found")

            fps_c = 1 / (time.time() - t)
            self.fps = 0.75 * self.fps + 0.25 * fps_c
            cv2.putText(originalFrame, str(self.fps), (590, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

            try:
                if (self.showConvexHull == True):
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        if (d > 0):
                            start = tuple(biggestContour[s][0])
                            end = tuple(biggestContour[e][0])
                            cv2.line(originalFrame, start, end, [0, 255, 0], 2)

                if (self.showHullDefects == True):
                    for s, e, f, d in defects_list:
                        start = tuple(biggestContour[s][0])
                        end = tuple(biggestContour[e][0])
                        far = tuple(biggestContour[f][0])
                        cv2.line(originalFrame, start, end, [0, 255, 0], 2)
                        midx = int((start[0] + end[0]) / 2)
                        midy = int((start[1] + end[1]) / 2)
                        midpoint = (midx, midy)
                        cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
                        cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)

                if (self.showHoughLines == True):
                    for line in filtered_lines:
                        cv2.line(gray, line[1], line[0], (0, 0, 255), 3, cv2.LINE_AA)
            except:
                print("Error showing one or more frames")

            if (self.visibleFloodfill == True):
                cv2.imshow("Floodfill", flooded_eges)
            if (self.visibleFrame == True):
                cv2.imshow("Frame", originalFrame)
            if (self.visibleEdges == True):
                cv2.imshow("Edges", edges)
            if (self.visibleGray == True):
                cv2.imshow("Gray", gray)

            k = cv2.waitKey(5) & 0xFF
            if k == 27:  # esc
                self.running = False
                break

            gesture = self.checkGesture(k)
            if gesture != -1:
                try:
                    data = self.cnt_hull_attributes(biggestContour)
                    data.append(numberOfDefects)
                    line_to_be_defined = 0
                    data.append(line_to_be_defined)
                    data.append(gesture)
                    self.dataframe.write(data)
                except:
                    print("Error writing to database")

        cap.release()
        cv2.destroyAllWindows()

    def checkGesture(self, k):
        gesture = -1
        if k == ord('1'):
            gesture = 1
        elif k == ord('2'):
            gesture = 2
        elif k == ord('3'):
            gesture = 3
        elif k == ord('4'):
            gesture = 4
        elif k == ord('5'):
            gesture = 5
        elif k == ord('0'):
            gesture = 0
        if gesture != -1:
            pass
            # print(gesture)
        return gesture

    def findEdges(self, gray, prev_edges, kernel):
        originalEdges = cv2.Canny(gray, self.lower, self.upper)
        edges_simple = originalEdges
        edges_simple[self.bottonLine:, :] = 0
        edges_simple = cv2.dilate(edges_simple, kernel, iterations=2)
        edges_simple = cv2.erode(edges_simple, kernel, iterations=2)

        try:
            edges = cv2.bitwise_or(edges_simple, cv2.erode(prev_edges, kernel, iterations=1))
        except:
            edges = edges_simple

        prev_edges = edges_simple
        edges = cv2.dilate(edges, kernel, iterations=2)
        edges = cv2.erode(edges, kernel, iterations=1)
        return [edges, prev_edges]

    def floodFillEdges(self, edges, prev_flooded):
        edges[self.bottonLine - 5, :] = 255
        floodfill = edges.copy()
        h, w = edges.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(floodfill, mask, (0, 0), 255);
        floodfill_inv = cv2.bitwise_not(floodfill)
        floodfill_inv[self.bottonLine - 5:, :] = 0
        floodfill_inv[:]
        try:
            floodfill = cv2.bitwise_or(floodfill_inv, prev_flooded)
        except:
            floodfill = floodfill_inv
        floodfill_prev = floodfill_inv
        return [floodfill, floodfill_prev]

    def filterHullDefects(self, defects):
        defects_list = []
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if (d > self.defectsSize):
                defects_list.append([s, e, f, d])
        return defects_list

    def filterLines(self, lines):
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

    def dictLines(self, lines):
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

    def cnt_hull_attributes(self, contour):
        hull = cv2.convexHull(contour)
        c_area = cv2.contourArea(contour)
        c_perimeter = cv2.arcLength(contour, True)
        hull_area = cv2.contourArea(hull)

        shape_factor = c_area / (c_perimeter ** 2)
        solidity = float(c_area) / hull_area
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        extent = c_area / (w * h)
        moment = cv2.moments(contour)

        attr_list = [shape_factor, solidity, aspect_ratio, extent]
        keys = ['nu02', 'nu03', 'nu11', 'nu12', 'nu20', 'nu21', 'nu30']
        for k in keys:
            attr_list.append(moment[k])
        return attr_list

    def angle(self, biggestContour):
        angle_acum = 0
        if (len(biggestContour) > 20):
            for i in range(1, biggestContour.shape[0] - 1):
                dx21 = biggestContour[i - 1][0][0] - biggestContour[i][0][0]
                dy21 = biggestContour[i - 1][0][1] - biggestContour[i][0][1]

                dx31 = biggestContour[i][0][0] - biggestContour[i + 1][0][0]
                dy31 = biggestContour[i][0][1] - biggestContour[i + 1][0][1]

                m12 = (dx21 ** 2 + dy21 ** 2)
                m13 = (dx31 ** 2 + dx31 ** 2)
                val = (dx21 * dx31 + dy21 * dy31) / (m12 * m13)
                if val >= 0.99:
                    angle = 0
                elif val <= -0.99:
                    angle = np.pi
                else:
                    angle = math.acos(val)
                angle_acum += angle

    def findContour(self, contours):
        maxArea = 0
        for cnt in contours:
            newArea = cv2.contourArea(cnt)
            if newArea > maxArea:
                maxArea = newArea
                biggestContour = cnt
        return biggestContour
