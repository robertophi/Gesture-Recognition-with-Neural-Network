import sys
import numpy as np
from collections import defaultdict
from PyQt5.QtCore import QThread
import cv2, time, math
import dataframe, pickle
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import pandas as pd

##

class ImageProcesser(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.upper = 200
        self.lower = 80
        self.thresh = 100
        self.minimumGray = 70
        self.defectsSize = 2500

        self.bottonLine = -120
        self.visibleFrame = True
        self.visibleEdges = True
        self.visibleGray = False
        self.visibleFloodfill = True
        self.showConvexHull = True
        self.showHullDefects = True
        self.drawContour = True
        self.showPredict = True
        self.pause = False
        self.dataframe = dataframe.DataFrame()
        self.MLP = 0
        self.scaler = 0

        self.fps = 0
        self.running = False
        self.destroyAllWindows = False

    def __del__(self):
        self.wait()

    #Perfomance analysis: 
    #@profile
    def run(self):
        self.running = True

        
        #Decidir qual a origem do vídeo: câmera ou arquivo
        camera = True
        
        
        
        if camera == True:
            cap = cv2.VideoCapture(0)
            video_delay = 0
        else:
            cap = cv2.VideoCapture('200-80-80-70-2500C.avi')
            video_delay = 0

        #Para salvar o vídeo que está sendo gravado, utiliza-se este video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('teste.avi',fourcc, 25.0, (640,480))

        #Algumas variáveis úteis durante todo o processo: máscaras, kerneis, etc
        mask = cv2.imread('mask.png',0)
        #kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel_ellipse=cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        font = cv2.FONT_HERSHEY_SIMPLEX
        prev_edges = -1
        prev_flooded_edges = -1
        


        #Carregando a rede neural salva em num arquivo pickle. Há também o escaler usado na rede neural
        try:
            pickle_in = open('mlp.pickle', 'rb')
            scaler_in = open('scaler.pickle', 'rb')

            self.MLP = pickle.load(pickle_in)
            self.scaler = pickle.load(scaler_in)

        except:
            print("Could not load classifier/scaler")

        

        while (self.running and cap.isOpened()):
            while(self.pause == True):
                print("Pause")
                time.sleep(0.25)
        
            if (self.destroyAllWindows == True):
                cv2.destroyAllWindows()
                self.destroyAllWindows = False
            t = time.time()
           
            
            # Captura os frames da fonte de vídeo
            ret, originalFrame = cap.read()
            if ret == False:
                print("Erro na leitura da câmera")
                self.running = False
                break
            
            #Escreve o frame no arquivo de video output
            out.write(originalFrame)

            #Delay caso o vídeo seja carregado de um arquivo (FPS limiter)
            time.sleep(video_delay/1000)
            
            #Aquisição da região de interesse, conversão para escala de cinza
            frame = originalFrame[:, 0:300]
            originalGray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            #Filtro gaussiano e correção gamma
            gray = cv2.GaussianBlur(originalGray, (3,3), 0)
            gray = self.gamma_correction(gray,2)
            
            #Transformação para imagem binária
            ret1, gray_thresh1 = cv2.threshold(gray,self.minimumGray,255, cv2.THRESH_TOZERO)
            ret2, gray_thresh2 = cv2.threshold(gray_thresh1,0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
      
            #Transformações morfológicas: sequência de erodes e dilates
            gray_mask = cv2.dilate(gray_thresh2, kernel_ellipse, iterations=1)
            gray_mask = cv2.erode(gray_mask, kernel_ellipse, iterations=1)
            gray_mask = cv2.dilate(gray_mask, kernel_ellipse, iterations=4)
            
            
            


            
            
            
            
            #Detecção da borda do objeto de interesse         
            
            # Original edges = apenas o edge obtido da imagem atual
            # Simple edge = edge da imagem atual processado
            # Previous edges = edges calculados das imagem anteriores
            edges, prev_edges = self.findEdges(gray_mask, prev_edges, kernel_ellipse)
            edges = cv2.bitwise_and(edges,mask)
            
            
            
            #Processo de "flood" das bordas, para obter um objeto sólido
            flooded_eges, prev_flooded_edges = self.floodFillEdges(edges, prev_flooded_edges)
            flooded_eges = cv2.dilate(flooded_eges,kernel_ellipse,iterations=2)
            
            #Detecção do maior contour disponível
            im2, contours, hierarchy = cv2.findContours(flooded_eges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            try:
                biggestContour = self.findContour(contours)
            except:
                print("Error na análise do contour")


                
            #Detecção do Convex Hull e o número de defects encontrados
            try:
                if self.drawContour == True:
                    cv2.drawContours(originalFrame, [biggestContour], -1, (255, 0, 0), 2)
                hull = cv2.convexHull(biggestContour, returnPoints=False)
                defects = cv2.convexityDefects(biggestContour, hull)
                defects_list = self.filterHullDefects(defects)
                numberOfDefects = len(defects_list)
            except:
                print("No contour found")

                
           


            #Display do convex hull e hull defects, caso selecionado
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
                        #cv2.line(originalFrame, start, end, [0, 255, 0], 2)
                        midx = int((start[0] + end[0]) / 2)
                        midy = int((start[1] + end[1]) / 2)
                        midpoint = (midx, midy)
                        cv2.line(originalFrame, midpoint, far, [0, 255, 125], 2)
                        cv2.circle(originalFrame, far, 5, [0, 0, 255], -1)

            except:
                print("Error drawing ConvexHull or HullDefects")

                
            #Aquisição de diversos descritores baseados no contour e convex hull
            try:
                data = self.cnt_hull_attributes(biggestContour)
                data.append(numberOfDefects)
                line_to_be_defined = 0
                data.append(line_to_be_defined)
            except:
                print("error getting data from contour")


            #Classificação preditiva da rede neural
            #Utiliza também o scaler carregado
            if self.showPredict == True:
                try:
                    temp = np.array(data).reshape((1, -1))
                    temp = self.scaler.transform(temp)
                    prediction = self.MLP.predict(temp)
                    cv2.putText(originalFrame, str(prediction), (50, 80), font, 1, (125, 255, 255), 2, cv2.LINE_AA)
                except:
                    cv2.putText(originalFrame, "[?]", (50, 80), font, 1, (125, 255, 255), 2, cv2.LINE_AA)
                    print("Could not classify")

            #Display de frames por segundo
            fps_c = 1 / (time.time() - t)
            self.fps = 0.75 * self.fps + 0.25 * fps_c
            cv2.putText(originalFrame, str(self.fps), (590, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

            
            #Display de imagens selecionadas
            if (self.visibleFloodfill == True):
                cv2.imshow("Floodfill", flooded_eges)
            if (self.visibleFrame == True):
                cv2.imshow("Frame", originalFrame)
            if (self.visibleEdges == True):
                cv2.imshow("Edges", edges)
            if (self.visibleGray == True):
                cv2.imshow("Gray", gray)
                cv2.imshow("Gray mask", gray_mask)

                
            #Controle do vídeo: apertar um botao no display realiza uma função
                #1 : adiciona a atual imagem no banco de dados, especificando o gesto "1"
                #2 : adiciona a atual imagem no banco de dados, especificando o gesto "2"
                #3 : adiciona a atual imagem no banco de dados, especificando o gesto "3"
                #4 : adiciona a atual imagem no banco de dados, especificando o gesto "4"
                #5 : adiciona a atual imagem no banco de dados, especificando o gesto "5"
                #0 : adiciona a atual imagem no banco de dados, especificando o gesto "0"
                #"esc" : para o programa
            k = cv2.waitKey(1) & 0xFF
            if k == 27:  # esc
                self.running = False
                break
            gesture = self.checkGesture(k)
            if gesture != -1:
                try:
                    data.append(gesture)
                    self.dataframe.write(data)
                except:
                    print("Error writing to database")


        cap.release()
        cv2.destroyAllWindows()

        
        
    #Identifica qual botão foi pressinado no display
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
        return gesture

    #Processo de correção gamma
    def gamma_correction(self,img, correction):
        img = img/255.0
        img = cv2.pow(img, correction)
        return np.uint8(img*255)
        
    #Detector de edges, utiliza o frame atual e o frame anterior, para realizar uma média
    # e diminuir o número de errors e ruido
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
        edges = cv2.erode(edges, kernel, iterations=2)
        return [edges, prev_edges]

    #Processo de floodfill da imagem produzida pelo findEdges
    #Também utiliza o frame atual e o frame anterior
    def floodFillEdges(self, edges, prev_flooded):
        edges[self.bottonLine - 5, :] = 255
        edges[:,-10:] = 0
        #edges[:,0:10] = 0
        floodfill = edges.copy()
        h, w = edges.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(floodfill, mask, (0, 0), 255)
        floodfill_inv = cv2.bitwise_not(floodfill)
        floodfill_inv[self.bottonLine - 5:, :] = 0
        try:
            floodfill = cv2.bitwise_or(floodfill_inv, prev_flooded)
        except:
            floodfill = floodfill_inv
        floodfill_prev = floodfill_inv
        return [floodfill, floodfill_prev]
        
        
    #Seleciona quais defects são interessante para a aplicação
    #Defects muito pequenos são provavelmente indesejados
    #Retorna o ponto inicial, final e outras propriedades de cada defect
    def filterHullDefects(self, defects):
        defects_list = []
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            if (d > self.defectsSize):
                defects_list.append([s, e, f, d])
        return defects_list

  

  
    #Calcula os diversos descritores a partir do maior contour encontrados
    #Shape factor
    #Solidity
    #Aspect ratio
    #Extent
    #Momentos (nu00 à nu30)
    #Utiliza área do contour e convex hull, perimetro do contour e convex hull
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


    #Encontra o maior contour na lista de contours encontrados
    def findContour(self, contours):
        maxArea = 0
        for cnt in contours:
            newArea = cv2.contourArea(cnt)
            if newArea > maxArea:
                maxArea = newArea
                biggestContour = cnt
        if(maxArea > 5000 and maxArea < 50000):
            return biggestContour
        else:
            return 0
