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
], columns = ['Nombre', 'Precio', 'Cantidad', 'Fecha de vencimiento'], index=['A1', 'A2', 'A3', 'A4', 'A5','B1', 'B2', 'B3', 'B4', 'B5','C1', 'C2', 'C3', 'C4', 'C5','D1', 'D2', 'D3', 'D4', 'D5','E1', 'E2', 'E3', 'E4', 'E5'])


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
        for i in range(self.columnCount()):
            header_item = QtWidgets.QTableWidgetItem(str(self.df.columns[i]))#str(self.df.index[0])
            self.setHorizontalHeaderItem(i,header_item)
        for i in range(self.rowCount()):
            header_item = QtWidgets.QTableWidgetItem(str(self.df.index[i]))#str(self.df.index[0])
            self.setVerticalHeaderItem(i,header_item)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if j==0:
                    x = str(self.df.iloc[i, j])
                    self.LineWidget = QLineEdit()
                    self.LineWidget.setPlaceholderText(x)
                    self.setCellWidget(i, j, self.LineWidget)
                elif j==2:
                    CantidadWidget= QComboBox()
                    CantidadWidget.addItems(["0", "1", "2","3","4","5"])
                    self.setCellWidget(i, j, CantidadWidget)
                elif j==3:
                    DateEditWidget= QDateTimeEdit()
                    self.setCellWidget(i, j, DateEditWidget)

                else:
                    x = float(self.df.iloc[i, j])
                    self.setItem(i, j, QTableWidgetItem(x))


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
        self.boton = QPushButton('Apply', self)
        self.layout.addWidget(self.boton)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.print_my_df)
        self.boton.clicked.connect(self.ApplyAction)

    @pyqtSlot()
    def print_my_df(self):
        print(self.tableWidget.df)
    def ApplyAction(self):
        print(self.tableWidget.rowCount())
        for i in range(self.tableWidget.rowCount()):
            for j in range(self.tableWidget.columnCount()):
                #self.tableWidget.setCurrentCell(i,j)
                if j==0:
                    nombre=str(self.tableWidget.cellWidget(i,j).text())
                    self.tableWidget.df.iloc[i,j]=nombre
                elif j==1:
                    nombre=self.tableWidget.item(i, j).text()
                    self.tableWidget.df.iloc[i,j]=nombre
                elif j==2:
                    nombre=str(self.tableWidget.cellWidget(i,j).currentText())
                    self.tableWidget.df.iloc[i,j]=nombre
                else:


                    nombre=str(self.tableWidget.cellWidget(i,j).sectionText(self.tableWidget.cellWidget(i,j).MonthSection))+'/'+str(self.tableWidget.cellWidget(i,j).sectionText(self.tableWidget.cellWidget(i,j).YearSection))
                    self.tableWidget.df.iloc[i,j]=nombre
                    #print('fecha')

 #       self.tableWidget.setCurrentCell(1,1)

  #      print(self.tableWidget.currentRow())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
