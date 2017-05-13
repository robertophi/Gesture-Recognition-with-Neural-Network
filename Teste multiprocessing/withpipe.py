

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
        self.pipe_in.send("asd")
        self.proc = multiprocessing.Process(target = self.run,args=())

    def start(self):
        self.proc.start()

    def run(self):
        while(1):
            print(self.pipe_out.recv())



def main():
    t = Teste()
    t.start()
    i=0
    while(1):
        t.pipe_in.send(str(i))
        i+=1


if __name__ == '__main__':
    main()