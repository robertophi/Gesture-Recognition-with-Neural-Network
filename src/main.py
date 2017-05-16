from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon

import sys # We need sys so that we can pass argv to QApplication
import time
import cv2

import mainwindow # This file holds our MainWindow and all design related things
                  # it also keeps events etc that we defined in Qt Designer

import imageProcesser




class ExampleApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Settings Configuration')
        self.setWindowIcon(QIcon('icon.png'))
        self.imgProc = imageProcesser.ImageProcesser()
        #self.start()


        self.pushButton_1.pressed.connect(self.start)
        self.pushButton_2.pressed.connect(self.stop)

        self.horizontalSlider_1.valueChanged.connect(self.Slider1)
        self.horizontalSlider_1.setValue(200) #upper
        self.horizontalSlider_2.valueChanged.connect(self.Slider2)
        self.horizontalSlider_2.setValue(80) #lower
        self.horizontalSlider_3.valueChanged.connect(self.Slider3)
        self.horizontalSlider_3.setValue(80) #thresh
        self.horizontalSlider_4.valueChanged.connect(self.Slider4)
        self.horizontalSlider_4.setValue(110) #min
        self.horizontalSlider_5.valueChanged.connect(self.Slider5)
        self.horizontalSlider_5.setValue(2500)


        self.checkBox_1.clicked.connect(self.checkbox_visible)
        self.checkBox_2.clicked.connect(self.checkbox_visible)
        self.checkBox_3.clicked.connect(self.checkbox_visible)
        self.checkBox_4.clicked.connect(self.checkbox_visible)
        self.checkBox_5.clicked.connect(self.checkbox_show)
        self.checkBox_6.clicked.connect(self.checkbox_show)
        self.checkBox_7.clicked.connect(self.checkbox_show)
        self.checkBox_8.clicked.connect(self.checkbox_show)

        self.checkBox_1.click()
        self.checkBox_2.click()
        self.checkBox_4.click()

        self.checkBox_5.click()
        self.checkBox_6.click()
        self.checkBox_7.click()


    def checkbox_visible(self):
        self.imgProc.visibleFrame = self.checkBox_1.isChecked()
        self.imgProc.visibleEdges = self.checkBox_2.isChecked()
        self.imgProc.visibleGray  = self.checkBox_3.isChecked()
        self.imgProc.visibleFloodfill = self.checkBox_4.isChecked()
        self.imgProc.destroyAllWindows = True
    def checkbox_show(self):
        self.imgProc.showConvexHull   = self.checkBox_5.isChecked()
        self.imgProc.showHullDefects  = self.checkBox_6.isChecked()
        self.imgProc.showHoughLines   = self.checkBox_7.isChecked()


    def Slider1(self):
        temp = self.horizontalSlider_1.value()
        self.imgProc.upper = temp
        self.lcdNumber_1.display(temp)
    def Slider2(self):
        temp = self.horizontalSlider_2.value()
        self.imgProc.lower = temp
        self.lcdNumber_2.display(temp)
    def Slider3(self):
        temp = self.horizontalSlider_3.value()
        self.imgProc.thresh = temp
        self.lcdNumber_3.display(temp)
    def Slider4(self):
        temp = self.horizontalSlider_4.value()
        self.imgProc.minLineSize = temp
        self.lcdNumber_4.display(temp)
    def Slider5(self):
        temp = self.horizontalSlider_5.value()
        self.imgProc.defectsSize = temp
        self.lcdNumber_5.display(temp)

    def start(self):
        self.imgProc.running = True
        self.imgProc.start()
        print("Start")

    def stop(self):
        #Deixar a cãmera desligar primeiro
        self.imgProc.running = False
        time.sleep(0.5)
        #Terminar o threadh
        self.imgProc.terminate()
        print("Stop")

    def keyPressEvent(self, e):
        #Escape = interrompe vídeo
        #Ctrl + Q = fecha o programa
        mod = QApplication.keyboardModifiers()
        if e.key() == Qt.Key_Escape:
            self.stop()
        elif e.key() == Qt.Key_Q:  #(e.key() == Qt.Key_Q) and (mod == Qt.ControlModifier):
            self.stop()
            QApplication.quit()
        elif(e.key() == Qt.Key_S):
            self.pressedS()

    def pressedS(self):
        if(self.imgProc.running == True):
            self.stop()
        else:
            self.start()


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function