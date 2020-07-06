import random
import time
from azure.iot.device import IoTHubDeviceClient, Message
import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QTimer,QDate, QTime, QDateTime
from PyQt5.QtGui import *


debug=False
str_seleccion=''
diferentes =[]

CONNECTION_STRING = "HostName=Proyecto-IE-Incrustados.azure-devices.net;DeviceId=MyPythonDevice;SharedAccessKey=SYD4n2ovYxHGgexe18gCE+wdfSN4SjMwzg/zDdAUmOw="

# Define the JSON message to send to IoT Hub.

MSG_TXT = '{{"Message Type": {msg_type},"Content": {data_str}}}'

data = pd.DataFrame([
['Galleta chicky',200,1.0,0],
['Merendina',150,3.0,0],
['',0,0,0],
['',0,0,0],
['Galleta chicky',200,2.0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
['',0,0,0],
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
                    self.LineWidget.insert(x)
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
        self.QWidget.labelName = QLabel()
        self.QWidget.labelMonto = QLabel()#AlignHCenter
        self.QWidget.labelName.setAlignment(Qt.AlignCenter)
        self.QWidget.labelMonto.setAlignment(Qt.AlignCenter)
        self.QWidget.layout.addWidget(self.QWidget.labelName)
        self.QWidget.layout.addWidget(self.QWidget.labelMonto)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.button = QPushButton('Cancelar', self)
        self.EfectivoWidget = QLineEdit()
        self.EfectivoWidget.setPlaceholderText('Ingrese el monto en efectivo')
        self.QWidget.layout.addWidget(self.EfectivoWidget)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.boton = QPushButton('Realizar pago', self)
        self.QWidget.layout.addWidget(self.QWidget.boton)
        self.QWidget.layout.addWidget(self.QWidget.button)
        self.QWidget.setLayout(self.QWidget.layout)
        self.QWidget.button.clicked.connect(self.print_my_df)
        self.QWidget.boton.clicked.connect(self.ApplyPayment)
        self.setGeometry(600, 600, 900, 700)
        self.setWindowTitle('Pago')
        self.setCentralWidget(self.QWidget)

    @pyqtSlot()
    def print_my_df(self):
        self.close()
    def ApplyPayment(self):
        global str_seleccion
        self.EfectivoWidget.setPlaceholderText('Ingrese el monto en efectivo')

        if is_number(self.EfectivoWidget.text()):
            efectivo= float(self.EfectivoWidget.text())
            #print(efectivo)
            #print(str_seleccion)

            self.pago(efectivo,str_seleccion)
        else:
            mensaje= 'Por favor ingrese un monto valido'
            self.showdialog(mensaje)
    def pago(self,efectivo,seleccion):
        datos_seleccion = seleccion.split('\n')
        datos_seleccion[0]#Aqui esta el nombre
        type= 'Sale Update:'
        current_status= 'Venta iniciada, producto: '+ str(datos_seleccion[0])
        msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=current_status)
        sendMessage(msg_txt_formatted)

        alcanza =True
        disponible = False
        cantidad_restante=0.0
        for i in range(len(data.index)):
            if self.df.iloc[i,0]==datos_seleccion[0]:
                if float(self.df.iloc[i,2])>0.0:
                    #alcanza
                    disponible=True
                    if (efectivo-float(self.df.iloc[i,1]))>=0.0:
                        alcanza=True
                        vuelto= efectivo-float(self.df.iloc[i,1])
                        self.df.iloc[i,2]= float(self.df.iloc[i,2])-1.0
                        #cantidad_restante=self.df.iloc[i,2]
                    else:
                        alcanza=False
                    break
                else:
                    disponible=False
        if disponible==True:
            if alcanza == True:
                type= 'Sale Update:'
                current_status= 'Producto: '+str(datos_seleccion[0])
                msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=current_status)
                sendMessage(msg_txt_formatted)
                mensaje= 'Muchas gracias por su compra, su vuelto es: '+ str(vuelto)
                self.showdialog(mensaje)
                self.close()
            else:
                mensaje= 'Dinero insuficiente.'
                self.showdialog(mensaje)
        else:
            mensaje= 'El producto no esta disponible.'
            type= 'Admin Update:'
            current_status= 'Producto '+str(datos_seleccion[0])+' no disponible '
            msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=current_status)
            sendMessage(msg_txt_formatted)
            self.showdialog(mensaje)

            self.close()

    def showdialog(self,mensaje):
       msg = QMessageBox()
       msg.setText(mensaje)
       msg.setWindowTitle("Mensaje")
       msg.setStandardButtons(QMessageBox.Ok)
       retval = msg.exec_()

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
            self.QWidget.button.clicked.connect(self.print_my_df)
        self.QWidget.boton = QPushButton('Apply', self)
        self.QWidget.layout.addWidget(self.QWidget.boton)
        self.QWidget.setLayout(self.QWidget.layout)
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
        type= 'Status Update:'
        current_status= 'Actualizacion de inventario'
        msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=current_status)
        #print('5s')
        sendMessage(msg_txt_formatted)
        self.close()

class Vendedor(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global data
        self.timer =QTimer()
        self.timer.start(60000)
        self.timer.timeout.connect(self.status)
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


    def status(self):
        global MSG_TXT
        global data
        data_list = []
        for i in range(len(data.index)):
            if data.iloc[i,0]=='':
                continue
            else:
                si_esta=False
                for k in range(len(data_list)):
                    if data.iloc[i,0]==data_list[k]:
                        data_list[k+1]=float(data_list[k+1])+float(data.iloc[i,2])
                        si_esta = True
                        break
                if si_esta==False:
                    data_list.append(data.iloc[i,0])
                    data_list.append(float(data.iloc[i,2]))
                    data_list.append(data.iloc[i,3])

        #print(data_list)


        type= 'Status Update:'
        msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=data_list)
        #print('5s')
        sendMessage(msg_txt_formatted)
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
            self.statusBar().showMessage('Ha seleccionado: '+sender.text())

        if int_Verify==5:
            type= 'Admin Login:'
            current_status= 'Iniciada administracion del producto'
            msg_txt_formatted = MSG_TXT.format(msg_type=type, data_str=current_status)
            sendMessage(msg_txt_formatted)
            self.admin_log()
            int_Verify=0

    def admin_log(self):
        print('admin')
        self.dialog.show()

    def transaccion(self,str_producto):
        datos_producto =str_producto.split('\n')
        self.dialogTransaccion.QWidget.labelName.setText('Ud ha seleccionado: '+ datos_producto[0])
        self.dialogTransaccion.QWidget.labelMonto.setText('El precio es: '+ datos_producto[1])
        self.dialogTransaccion.EfectivoWidget.clear()
        self.dialogTransaccion.show()
def sendMessage(msg_txt_formatted):
    try:
        client = iothub_client_init()
        message = Message(msg_txt_formatted)
        client.send_message(message)
        client.disconnect()

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
def iothub_client_init():
        # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def main():
    app = QApplication(sys.argv)
    ex = Vendedor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    main()

    #iothub_client_telemetry_sample_run()
