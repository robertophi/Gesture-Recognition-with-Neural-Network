
import numpy as np
from collections import defaultdict
from PyQt5.QtCore import QThread
import cv2, time, math


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
        self.visibleGray = True
        self.showConvexHull = True
        self.showHullDefects = True
        self.showHoughLines = True

        self.fps = 0
        self.running = False
        self.destroyAllWindows = False

    def __del__(self):
        self.wait()

    def run(self):
        self.running = True

        #cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture('output.avi')

        kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #kernel_ellipse=cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        font = cv2.FONT_HERSHEY_SIMPLEX
        prev_edges = -1
        prev_flooded_edges = -1
        while (self.running and cap.isOpened()):
            if(self.destroyAllWindows == True):
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
            ##########################################




            ##########################################
            # Original edges = apenas o edge obtido da imagem atual
            # Simple edge = edge da imagem atual processado
            # Previous edges = edges calculados das imagem anteriores

            edges, prev_edges = self.findEdges(gray,prev_edges, kernel_ellipse)
            flooded_eges, prev_flooded_edges = self.floodFillEdges(edges,prev_flooded_edges)




            cv2.imshow("Fill", flooded_eges)

            im2, contours, hierarchy = cv2.findContours(flooded_eges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ##########################################





            ##########################################
            try:
                lines = cv2.HoughLines(image=edges, rho=10,
                                       theta=np.pi / 6, threshold=30)
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
                ##########################################





                ##########################################
            maxArea = 0
            for cnt in contours:
                newArea = cv2.contourArea(cnt)
                if newArea > maxArea:
                    maxArea = newArea
                    biggestContour = cnt

            try:
                cv2.drawContours(originalFrame,[biggestContour],-1,(255,0,0),2)
                hull = cv2.convexHull(biggestContour, returnPoints=False)
                defects = cv2.convexityDefects(biggestContour, hull)
                defects_list = self.filterHullDefects(defects)
            except:
                print("No contour found")
                ##########################################
            fps_c = 1/(time.time()-t)
            self.fps = 0.75*self.fps + 0.25*fps_c
            cv2.putText(originalFrame, str(self.fps), (590, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            try:
                if(self.showConvexHull == True):
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        if (d > 0):
                            start = tuple(biggestContour[s][0])
                            end = tuple(biggestContour[e][0])
                            cv2.line(originalFrame, start, end, [0, 255, 0], 2)

                if(self.showHullDefects == True):
                    for s,e,f,d in defects_list:
                        start = tuple(biggestContour[s][0])
                        end = tuple(biggestContour[e][0])
                        far = tuple(biggestContour[f][0])
                        cv2.line(originalFrame, start, end, [0, 255, 0], 2)
                        midx = int((start[0] + end[0]) / 2)
                        midy = int((start[1] + end[1]) / 2)
                        midpoint = (midx, midy)
                        cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
                        cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)

                if(self.showHoughLines == True):
                    for line in filtered_lines:
                        cv2.line(gray, line[1], line[0], (0, 0, 255), 3, cv2.LINE_AA)
            except:
                print("cant show")

            if(self.visibleFrame==True):
                cv2.imshow("Frame", originalFrame)
            if(self.visibleEdges == True):
                cv2.imshow("Edges", edges)
            if(self.visibleGray==True):
                cv2.imshow("Gray", gray)

            k = cv2.waitKey(5) & 0xFF
            if k == 27: #esc
                self.running = False
                break

        cap.release()
        cv2.destroyAllWindows()

    def findEdges(self, gray, prev_edges, kernel):

        originalEdges = cv2.Canny(gray, self.lower, self.upper)
        edges_simple = originalEdges
        edges_simple[self.bottonLine:, :] = 0
        edges_simple = cv2.dilate(edges_simple, kernel, iterations=4)
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
        try:
            floodfill = cv2.bitwise_or(floodfill_inv, prev_flooded)
        except:
            floodfill = floodfill_inv
        floodfill_prev = floodfill_inv
        return [floodfill, floodfill_prev]


    def filterHullDefects(self, defects):
        defects_index_list = []
        defects_list = []
        max = 0
        max_index = -1
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if (d > self.defectsSize):
                print(d)
                if d>max:
                    max = d
                    max_index = i
                defects_index_list.append(i)
        defects_index_list.remove(max_index)
        for j in defects_index_list:
            s,e,f,d = defects[j,0]
            defects_list.append([s,e,f,d])
        return defects_list


    def filterLines(self,lines):
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
            if size > 5000 and size < 25000:
                filtered_lines.append(((xi,yi),(xf,yf)))
        return filtered_lines


    def dictLines(self,lines):
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

    def cnt_hull_attributes(self,contour):
        hull = cv2.convexHull(contour)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        extent = area / (w * h)
        moment = cv2.moments(contour)
        attr_dict = {"area": area,
                     "perimeter": perimeter,
                     "solitidy": solidity,
                     "aspect_ratio": aspect_ratio,
                     "extent": extent}
        for i in moment.keys():
            if i[0] == "n":
                attr_dict[i] = moment[i]
        return attr_dict


    def angle(self,biggestContour):
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