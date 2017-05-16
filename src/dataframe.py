import pandas as pd
import numpy as np
import os

import csv

class DataFrame():
    def __init__(self):
        self.colunas = ["Shape Factor","Solidity","Aspect Ratio","Extent",'nu02','nu03','nu11','nu12','nu20','nu21','nu30',"Hull defects","Line","Gesture"]
        if os.listdir().__contains__("dataframe.csv") == False:
            csvFile = open('dataframe.csv', 'a', newline='')
            csvWriter = csv.writer(csvFile, dialect='excel')
            csvWriter.writerow(self.colunas)

    def write(self, values):
        if len(values) != len(self.colunas):
            print("Erro ao adicionar linha à dataframe: tamanho incompatível")
        else:
            if all(type(item)==int or type(item) == float for item in values):
                csvFile = open('dataframe.csv', 'a', newline='')
                csvWriter = csv.writer(csvFile, dialect='excel')
                csvWriter.writerow(values)
                csvFile.close()
            else:
                print("Erro ao adicionar linha à dataframe: tipo do valor incorreto (not float/int)")

    def read(self):
        File = open('dataframe.csv')
        Reader = csv.reader(File)
        for row in Reader:
            print('#' + str(Reader.line_num) + ' ' + str(row))
        File.close()