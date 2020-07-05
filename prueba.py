import sys
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import *

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
                x = str(self.df.iloc[i, j])
                self.setItem(i, j, QTableWidgetItem(x))

        self.cellChanged.connect(self.onCellChanged)

    @pyqtSlot(int, int)
    def onCellChanged(self, row, column):
        text = self.item(row, column).text()
        number = float(text)
        self.df.set_value(row, column, number)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 100, 350, 380)
        df_rows = 10
        df_cols = 3
        df = pd.DataFrame(np.random.randn(df_rows, df_cols))
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
