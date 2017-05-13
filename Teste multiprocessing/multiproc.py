from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
import sys # We need sys so that we can pass argv to QApplication
import time
import multiprocessing
import cv2

                  # it also keeps events etc that we defined in Qt Designer

class Teste():
    def __init__(self):

        self.running = False
        self.pipe_out, self.pipe_in = multiprocessing.Pipe()
        self.proc = multiprocessing.Process(target = self.run,args=())

    def start(self):
        self.proc.start()

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)
        while(self.running):
            ret, frame = cap.read()
            cv2.imshow("Frame",frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                self.running = False
        cap.release()
        cv2.destroyAllWindows()



def main():
    t = Teste()
    t.start()
    while(1):
        print("aa")


if __name__ == '__main__':
    main()