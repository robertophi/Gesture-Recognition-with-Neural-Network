from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
import sys # We need sys so that we can pass argv to QApplication
import time
import cv2

import mainwindow # This file holds our MainWindow and all design related things
                  # it also keeps events etc that we defined in Qt Designer

import imageProcesser




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


        self.checkBox_1.clicked.connect(self.checkbox_all)
        self.checkBox_2.clicked.connect(self.checkbox_all)
        self.checkBox_3.clicked.connect(self.checkbox_all)
        self.checkBox_4.clicked.connect(self.checkbox_all)
        self.checkBox_5.clicked.connect(self.checkbox_all)
        self.checkBox_6.clicked.connect(self.checkbox_all)
        self.checkBox_7.clicked.connect(self.checkbox_all)
        self.checkBox_8.clicked.connect(self.checkbox_all)

        self.checkBox_1.click()
        self.checkBox_2.click()
        self.checkBox_3.click()



    def checkbox_all(self):
        self.imgProc.visibleFrame = self.checkBox_1.isChecked()
        self.imgProc.visibleEdges = self.checkBox_2.isChecked()
        self.imgProc.visibleGray = self.checkBox_3.isChecked()

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
        print("Nothing on slider 5")

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
        if e.key() == Qt.Key_Escape:
            self.stop()
        mod = QApplication.keyboardModifiers()
        if (e.key() == Qt.Key_Q) and (mod == Qt.ControlModifier):
            self.stop()
            QApplication.quit()




def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function