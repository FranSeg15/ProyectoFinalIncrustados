import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QTimer,QDate, QTime, QDateTime
from PyQt5.QtGui import *


data = pd.DataFrame([
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
], columns = ['Nombre', 'Cantidad', 'Precio', 'Fecha de vencimiento'], index=['A1', 'A2', 'A3', 'A4', 'A5','B1', 'B2', 'B3', 'B4', 'B5','C1', 'C2', 'C3', 'C4', 'C5','D1', 'D2', 'D3', 'D4', 'D5','E1', 'E2', 'E3', 'E4', 'E5'])


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class FloatDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent=parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setValidator(QDoubleValidator())
        return editor


class TableWidget(QTableWidget):
    def __init__(self, df, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = df
        nRows = len(self.df.index)
        nColumns = len(self.df.columns)
        self.setRowCount(nRows)
        self.setColumnCount(nColumns)
        self.setItemDelegate(FloatDelegate())

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if j==0:
                    x = str(self.df.iloc[i, j])
                    self.LineWidget = QLineEdit()
                    self.LineWidget.setPlaceholderText(x)

                    #tableWidget_F = QTableWidgetItem()
                    #self.LineWidget.textChanged.connect(self.pruebF)


                    self.setCellWidget(i, j, self.LineWidget)
                    self.cellActivated.connect(self.pruebaF)
                    #self.cellWidget(i,j).textChanged.connect(self.pruebF)
                    #self.item(i, j).textChanged.connect(self.pruebF)

                elif j==3:
                    x= QDate.currentDate()
                    DateEditWidget= QDateEdit()
                    fecha = QTableWidgetItem(x.toString())
                    self.setCellWidget(i, j, DateEditWidget)
                    #self.setItem(i, j, fecha)
                    self.cellChanged.connect(self.onCellChanged)
                else:
                    x = float(self.df.iloc[i, j])
                    self.setItem(i, j, QTableWidgetItem(x))
                    self.cellActivated.connect(self.pruebaF)
                   # self.cellChanged.connect(self.onCellChanged)

        #self.itemChange.connect(fecha,pruebaF)
        #self.cellChanged.connect(self.onCellChanged)

    @pyqtSlot(int, int)
    def onCellChanged(self, row, column):
        #self.LineWidget.textChanged.connect(self.pruebF)
        text = self.item(row, column).text()
        #print(text)
        if is_number(text):
            number = float(text)
        else:
            number = text
        self.df.iloc[row, column]= str(number)

    def pruebaF(self,row, column):
        #print(str(self.cellWidget(row,column).text()))
        #print (self.currentRow())

        self.df.iloc[self.currentRow(), 0]= str(self.cellWidget(row,column).text())
        #print(" ", s)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 100, 350, 380)
        df_rows = 10
        df_cols = 3
        global data
        df = data
        self.tableWidget = TableWidget(df, self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.button = QPushButton('Print DataFrame', self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.print_my_df)

    @pyqtSlot()
    def print_my_df(self):
        print(self.tableWidget.df)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
