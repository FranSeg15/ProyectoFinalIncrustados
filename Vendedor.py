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
from PyQt5.QtCore import pyqtSlot, Qt, QTimer,QDate, QTime, QDateTime
from PyQt5.QtGui import *


debug=True
int_Verify =0
str_seleccion=''
diferentes =[]
data = pd.DataFrame([
['Banano',1000,1,0],
['N/A',0,0,0],
['N/A',0,0,0],
['N/A',0,0,0],
['Banano',1000,2,0],
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
                    if is_number( self.df.iloc[i,j]):
                        x = float(self.df.iloc[i, j])
                    else:
                        x = str(self.df.iloc[i, j])
                    self.setItem(i, j, QTableWidgetItem(x))

class TransaccionW(QMainWindow):
    def __init__(self, parent=None):
        super(TransaccionW, self).__init__(parent)
        self.initUI()
    def initUI(self):
        global data
        self.QWidget = QWidget()
        self.df = data


        self.QWidget.layout = QVBoxLayout()
        if debug ==True:
            self.QWidget.button = QPushButton('Print DataFrame', self)
            self.QWidget.layout.addWidget(self.QWidget.button)
            self.QWidget.setLayout(self.QWidget.layout)
        self.EfectivoWidget = QLineEdit()
        self.EfectivoWidget.setPlaceholderText('Ingrese el monto en efectivo')
        self.QWidget.layout.addWidget(self.EfectivoWidget)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.boton = QPushButton('Realizar pago', self)
        self.QWidget.layout.addWidget(self.QWidget.boton)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.button.clicked.connect(self.print_my_df)
        self.QWidget.boton.clicked.connect(self.ApplyPayment)
        self.setGeometry(600, 600, 900, 700)
        self.setWindowTitle('Pago')
        self.setCentralWidget(self.QWidget)

    @pyqtSlot()
    def print_my_df(self):
        print(self.df)
    def ApplyPayment(self):
        global str_seleccion
        self.EfectivoWidget.setPlaceholderText('Ingrese el monto en efectivo')

        if is_number(self.EfectivoWidget.text()):
            efectivo= float(self.EfectivoWidget.text())
            #print(efectivo)
            #print(str_seleccion)
            self.pago(efectivo,str_seleccion)
        else:
            self.showdialog()
    def pago(self,efectivo,seleccion):

        datos_seleccion = seleccion.split('\n')
        datos_seleccion[0]#Aqui esta el nombre
        alcanza =True
        disponible = False
        for i in range(len(data.index)):
            if self.df.iloc[i,0]==datos_seleccion[0]:
                if float(self.df.iloc[i,2])>0.0:
                    #alcanza
                    disponible=True
                    if (efectivo-float(self.df.iloc[i,1]))>0.0:
                        alcanza=True
                        vuelto=-efectivo-self.df.iloc[i,1]
                        self.df.iloc[i,2]= float(self.df.iloc[i,2])-1.0
                    else:
                        alcanza=False
                    break
                else:
                    disponible=False
        if disponible==True:
            if alcanza == True:


    def showdialog(self,mensaje):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)

       msg.setText(efectivo)
       #msg.setInformativeText("This is additional information")
       msg.setWindowTitle("Error de digitacion")
       #msg.setDetailedText("The details are as follows:")
       msg.setStandardButtons(QMessageBox.Ok)
       #msg.buttonClicked.connect(self.msgbtn)

       retval = msg.exec_()
       #print ("value of pressed message box button:", retval)

    #def msgbtn(self,i):
      # print ("Button pressed is:",i.text())

class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.initUI()
    def initUI(self):
        global data
        self.QWidget = QWidget()
        df = data
        self.QWidget.tableWidget = TableWidget(df, self)


        self.QWidget.layout = QVBoxLayout()
        self.QWidget.layout.addWidget(self.QWidget.tableWidget )
        if debug ==True:
            self.QWidget.button = QPushButton('Print DataFrame', self)
            self.QWidget.layout.addWidget(self.QWidget.button)
            self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.boton = QPushButton('Apply', self)
        self.QWidget.layout.addWidget(self.QWidget.boton)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.button.clicked.connect(self.print_my_df)
        self.QWidget.boton.clicked.connect(self.ApplyAction)
        self.setGeometry(600, 600, 900, 700)
        self.setWindowTitle('Administracion de producto')
        self.setCentralWidget(self.QWidget)

    @pyqtSlot()
    def print_my_df(self):
        print(self.QWidget.tableWidget.df)
    def ApplyAction(self):
        for i in range(self.QWidget.tableWidget.rowCount()):
            for j in range(self.QWidget.tableWidget.columnCount()):
                if j==0:
                    nombre=str(self.QWidget.tableWidget.cellWidget(i,j).text())
                    self.QWidget.tableWidget.df.iloc[i,j]=nombre
                elif j==1:
                    nombre=self.QWidget.tableWidget.item(i, j).text()
                    self.QWidget.tableWidget.df.iloc[i,j]=nombre
                elif j==2:
                    nombre=str(self.QWidget.tableWidget.cellWidget(i,j).currentText())
                    self.QWidget.tableWidget.df.iloc[i,j]=nombre
                else:
                    nombre=str(self.QWidget.tableWidget.cellWidget(i,j).sectionText(self.QWidget.tableWidget.cellWidget(i,j).MonthSection))+'/'+str(self.QWidget.tableWidget.cellWidget(i,j).sectionText(self.QWidget.tableWidget.cellWidget(i,j).YearSection))
                    self.QWidget.tableWidget.df.iloc[i,j]=nombre
        self.close()

class Vendedor(QMainWindow):
    int_Verify =0;

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global data

        opciones = QWidget()
        grid = QGridLayout()
        opciones.setLayout(grid)
        #Aqui ocupo metodo para noombres
        Botones = ['A1', 'A2', 'A3', 'A4',
                 'A5', 'B1', 'B2', 'B3',
                 'B4', 'B5', 'C1', 'C2',
                 'C3', 'C4', 'C5','D1', 'D2', 'D3',
                 'D4', 'D5', 'E1', 'E2',
                 'E3', 'E4', 'E5']
        names = ['A1', 'A2', 'A3', 'A4',
                  'A5', 'B1', 'B2', 'B3',
                  'B4', 'B5', 'C1', 'C2',
                  'C3', 'C4', 'C5','D1', 'D2', 'D3',
                  'D4', 'D5', 'E1', 'E2',
                  'E3', 'E4', 'E5','','','','Pagar','Cancelar',]
        for i in range(25):
            if data.iloc[i,0]!="":
                names[i]=data.iloc[i,0]+'\n'+str(data.iloc[i,1])
            else:
                names[i]=''
        positions = [(i, j) for i in range(6) for j in range(5)]
        diferentes=[]
        diferentes.append(' ')
        for position, name in zip(positions, names):
            repetido=False
            for i in range(len(diferentes)):
                   if diferentes[i]==name:
                       repetido=True
            if name == '':
                continue
            elif repetido==True:
                continue
            else:
                button = QPushButton(name)
                button.clicked.connect(self.buttonClicked)
                grid.addWidget(button, *position)
                diferentes.append(name)
        self.statusBar()
        self.dialog= Second(self)
        self.dialogTransaccion= TransaccionW(self)
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
            self.initUI()
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
        self.dialogTransaccion.show()


def main():
    global int_Verify
    app = QApplication(sys.argv)
    ex = Vendedor()
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
