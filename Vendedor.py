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

#from PyQt5.QtWidgets import (QWidget, QTableWidget,QTableWidgetItem,QGridLayout,QPushButton, QApplication, QMainWindow, QMessageBox)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *


int_Verify =0;
data = pd.DataFrame([
[1, 9, 2],
[1, 0, -1],
[3, 5, 2],
[3, 3, 2],
[5, 8, 9],
], columns = ['A', 'B', 'C'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])



class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.initUI()
    def initUI(self):
        tabla = QWidget()
        self.table = self.tableWidget()
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        box = QVBoxLayout()

        #box.addWidget(self.tableWidget)
       # tabla.setLayout(box)
        #self.setLayout(self.layout)
        #self.setCentralWidget(tabla)


        self.setCentralWidget(self.table)
        self.setGeometry(600, 600, 900, 700)
        #opciones.show()
        self.setWindowTitle('Admin')
        # Show widget
        #self.show()

    def createTable(self):
       # Create table
       global data
       self.model = TableModel(data)
       self.table.setModel(self.model)
       self.model = TableModel(data)
       self.table.setModel(self.model)
        #self.tableWidget = QTableWidget()
        ##self.tableWidget.setRowCount(25)
        #self.tableWidget.setColumnCount(4)
        #self.tableWidget.setItem(0,0, QTableWidgetItem("A1"))
        #self.tableWidget.setItem(1,0, QTableWidgetItem("A2"))
        #self.tableWidget.setItem(2,0, QTableWidgetItem("A3"))
        #self.tableWidget.setItem(3,0, QTableWidgetItem("A4"))
        #self.tableWidget.setItem(4,0, QTableWidgetItem("A5"))
        #self.tableWidget.setItem(5,0, QTableWidgetItem("Cell (3,2)"))
        #self.tableWidget.setItem(6,0, QTableWidgetItem("Cell (4,1)"))
        #self.tableWidget.setItem(7,0, QTableWidgetItem("Cell (4,2)"))
        #self.tableWidget




       #self.tableWidget.move(0,0)

        # table selection change
       #self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

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
        self.setWindowTitle('Calculator')
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
