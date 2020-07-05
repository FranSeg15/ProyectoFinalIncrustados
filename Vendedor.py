#!/usr/bin/python

"""
ZetCode PyQt5 tutorial

In this example, we create a skeleton
of a calculator using QGridLayout.

Author: Jan Bodnar
Website: zetcode.com
"""

import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import *



int_Verify =0;
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
        for i in range(self.columnCount()):
            header_item = QtWidgets.QTableWidgetItem(str(self.df.columns[i]))#str(self.df.index[0])
            self.setHorizontalHeaderItem(i,header_item)
        for i in range(self.rowCount()):
            header_item = QtWidgets.QTableWidgetItem(str(self.df.index[i]))#str(self.df.index[0])
            self.setVerticalHeaderItem(i,header_item)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                x = str(self.df.iloc[i, j])
                papa = QTableWidgetItem(str(x))
                self.setItem(i, j,papa)

        self.cellChanged.connect(self.onCellChanged)

    @pyqtSlot(int,int)
    def onCellChanged(self, row, column):
        text = self.item(row, column).text()
        print ('Row: ' , row ,'Column: ' , column,' ', text  )
        if is_number(text):
            number = float(text)
        else:
            number = 'assad'
        self.df.iloc[row, column]= str(number)
        print(self.df)


class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.initUI()
    def initUI(self):
        global data
        self.QWidget = QWidget()
        df_rows = 10
        df_cols = 3
        df = data
        self.QWidget.tableWidget = TableWidget(df, self)
        self.setGeometry(700, 100, 350, 380)

        self.QWidget.layout = QVBoxLayout()
        self.QWidget.layout.addWidget(self.QWidget.tableWidget )
        self.QWidget.button = QPushButton('Print DataFrame', self)
        self.QWidget.layout.addWidget(self.QWidget.button)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.button.clicked.connect(self.print_my_df)
        self.setGeometry(600, 600, 900, 700)
        self.setWindowTitle('Administracion de producto')
        self.setCentralWidget(self.QWidget)

    @pyqtSlot()
    def print_my_df(self):
        print(self.QWidget.tableWidget.df)



class Vendedor(QMainWindow):
    int_Verify =0;

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        opciones = QWidget()
        grid = QGridLayout()
        opciones.setLayout(grid)
        #Aqui ocupo metodo para noombres
        names = ['Cls', 'Bck', 'ppp', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+','-',
                 '0', '.', '=', '+','','','','Pagar','Cancelar',]
        positions = [(i, j) for i in range(6) for j in range(5)]

        for position, name in zip(positions, names):

            if name == '':
                continue
            button = QPushButton(name)
            button.clicked.connect(self.buttonClicked)
            grid.addWidget(button, *position)

        #opciones.move(300, 150)

        self.statusBar()
        self.dialog= Second(self)
        self.setCentralWidget(opciones)
        self.setGeometry(600, 600, 900, 700)
        #opciones.show()
        self.setWindowTitle('Vendedor')
        self.show()

    def buttonClicked(self):
        global int_Verify
        global str_seleccion
        sender = self.sender()
        if sender.text() == "Close":
            print("close")
            sys.exit()
        elif sender.text() == "Cancelar":
            str_seleccion=''
            int_Verify=int_Verify+1
        elif sender.text() == "Pagar":
            if str_seleccion!='':
               self.transaccion(str_seleccion)


        else:
            str_seleccion=sender.text()
            int_Verify=0
        if int_Verify==5:
            self.admin_log()
            int_Verify=0
        self.statusBar().showMessage(sender.text() + ' was pressed')
    def admin_log(self):
        print('admin')
        self.dialog.show()

    def transaccion(self,str_producto):
        print('aa '+str_producto )

def main():
    global int_Verify
    app = QApplication(sys.argv)
    ex = Vendedor()
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
