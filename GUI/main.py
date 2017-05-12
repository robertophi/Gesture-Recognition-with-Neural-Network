from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
import sys # We need sys so that we can pass argv to QApplication
import time
import cv2
import threading

import mainwindow # This file holds our MainWindow and all design related things
              # it also keeps events etc that we defined in Qt Designer

class Teste():
    def __init__(self):
        self.upper = 110
        self.lower = 80
        self.thresh = 100
        self.minLineSize = 30

        self.visibleFrame = False
        self.visibleEdges = False
        self.visibleGray = False

    def show(self):
        print("Sliders:",self.upper,self.lower,self.thresh,self.minLineSize)
        print("Checkboxes:", self.visibleFrame,self.visibleEdges,self.visibleGray)

    def loop(self):
        cap = cv2.VideoCapture(0)
        while(1):
            ret, frame = cap.read()
            cv2.imshow("Frame",frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

class ExampleApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        self.setWindowTitle('Settings Configuration')

        self.t = Teste()

        self.t.loop()


        self.horizontalSlider_1.valueChanged.connect(self.Slider1)
        self.horizontalSlider_2.valueChanged.connect(self.Slider2)
        self.horizontalSlider_3.valueChanged.connect(self.Slider3)
        self.horizontalSlider_4.valueChanged.connect(self.Slider4)
        self.horizontalSlider_5.valueChanged.connect(self.Slider5)
        self.checkBox_1.clicked.connect(self.checkbox1)


    def thread_loop(self):
        t = threading.Thread(target=main)
        t.daemon = True
        t.start()
        loop = self.t.loop()
        
    def checkbox1(self):
        self.t.visibleFrame = self.checkBox_1.isChecked()
        self.t.visibleEdges = self.checkBox_2.isChecked()
        self.t.visibleGray = self.checkBox_3.isChecked()

    def Slider1(self):
        temp = self.horizontalSlider_1.value()
        self.t.upper = temp
        self.lcdNumber_1.display(temp)
    def Slider2(self):
        temp = self.horizontalSlider_2.value()
        self.t.lower = temp
        self.lcdNumber_2.display(temp)
    def Slider3(self):
        temp = self.horizontalSlider_3.value()
        self.t.thresh = temp
        self.lcdNumber_3.display(temp)
    def Slider4(self):
        temp = self.horizontalSlider_4.value()
        self.t.minLineSize = temp
        self.lcdNumber_4.display(temp)
    def Slider5(self):
        self.t.show()




def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function