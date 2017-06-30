import pandas as pd
import numpy as np
import os

import csv
'''
csvFile = open('example.csv', 'a', newline='')
csvWriter = csv.writer(csvFile, dialect='excel')
csvWriter.writerow(['A', 'B', 'C'])
csvWriter.writerow(['1', '2', '4'])
csvWriter.writerow(['12', '23', '45'])
csvFile.close()

exampleFile = open('example.csv')
exampleReader = csv.reader(exampleFile)
for row in exampleReader:
    print('Row #' + str(exampleReader.line_num) + ' ' + str(row))
'''

class DataFrame():
    def __init__(self):
        self.colunas = ["cnt_area","cnt_perim","u00","u01"]


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