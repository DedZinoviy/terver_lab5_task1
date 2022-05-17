from statisticalDataSmallArray import Statistic
import numpy as np
from PyQt5 import QtWidgets, QtCore
from ui import Ui_MainWindow
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from enum import Enum

class PoligonType(Enum):
    FREQUENCY = 0
    PERIODICITY = 1

class mywindow(QtWidgets.QMainWindow):
    '''Конструктор гловного окна'''
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.pen = pg.mkPen(color='r', width=3)
        self.pen1 = pg.mkPen(color='r', width=2, style=QtCore.Qt.DashLine)
        self.style1 = {'font-size':'30px'}
        
        self.ui.graphWidget.setBackground((225, 225, 225))
        self.ui.graphWidget.showGrid(x=True, y=True, alpha=1)

        self.ui.plotType.currentIndexChanged.connect(self.buildPlot)
        self.ui.openFileAction.triggered.connect(self.openFile)

        self.statistic = Statistic()
        

    def openFile(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть файл", "./", "Text file (*.txt)")
        fileName = fileName[0]

        try:
            file = open(fileName, 'r', encoding='utf-8')
            line = file.readline()
            
            serias = line.split(' ')
            serias = [int(var) for var in serias]
            self.statistic.setSeriesList(serias)
            
            string_serias = ", ".join(str(var) for var in self.statistic.variation_range)
            self.ui.variationSeriesText.setText(string_serias)
        except:
            QtWidgets.QMessageBox.warning(self, "Ошибка ввода", "Ошибка ввода!\nПроверьте корректность входного файла")

        self.solve()

    
    def solve(self):
        self.setTables()
        self.buildPlot()
        self.setFunction()
        self.setCharacteristic()

    
    def buildPlot(self):
        plotType = self.ui.plotType.currentIndex()
        var = self.statistic.variants
        n = self.statistic.frequency_range
        w = self.statistic.relative_frequency_range
        f = self.statistic.distribution_function

        self.ui.graphWidget.clear()
        if (plotType == 0):
            self.plotPoligon(var, n, PoligonType.FREQUENCY)
        elif (plotType == 1):
            self.plotPoligon(var, w, PoligonType.PERIODICITY)
        else:
            self.plotDistributionFunction(var, f)
        

    def setTables(self):
        columnCount = len(self.statistic.variants)
        self.ui.frequencyTable.setColumnCount(columnCount)
        self.ui.periodicityTable.setColumnCount(columnCount)

        variationSerias = self.statistic.variants
        frequency = self.statistic.frequency_range
        periodicity = self.statistic.relative_frequency_range

        for i in range(columnCount):
            var = "%g" % variationSerias[i]
            frec = "%g" % frequency[i]
            per = "%g" % periodicity[i]
            
            sectionFrequencySize = max(len(var), len(frec)) * 12
            self.ui.frequencyTable.horizontalHeader().resizeSection(i, sectionFrequencySize)
            self.ui.frequencyTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(''))

            self.ui.frequencyTable.setItem(0, i, QtWidgets.QTableWidgetItem(var))
            self.ui.frequencyTable.item(0, i).setFlags(QtCore.Qt.ItemIsEnabled)

            self.ui.frequencyTable.setItem(1, i, QtWidgets.QTableWidgetItem(frec))
            self.ui.frequencyTable.item(1, i).setFlags(QtCore.Qt.ItemIsEnabled)
            
            sectionPeriodicitySize = max(len(var), len(per)) * 12
            self.ui.periodicityTable.horizontalHeader().resizeSection(i, sectionPeriodicitySize)
            self.ui.periodicityTable.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(''))
            
            self.ui.periodicityTable.setItem(0, i, QtWidgets.QTableWidgetItem(var))
            self.ui.periodicityTable.item(0, i).setFlags(QtCore.Qt.ItemIsEnabled)
            
            self.ui.periodicityTable.setItem(1, i, QtWidgets.QTableWidgetItem(per))
            self.ui.periodicityTable.item(1, i).setFlags(QtCore.Qt.ItemIsEnabled)


    def setFunction(self):
        string_function = ""
        patern_string = "%g, при %d < x ≤ %d"
        amount = len(self.statistic.variants)
        var = self.statistic.variants
        f = self.statistic.distribution_function

        string_function += "0, при x ≤ " + str(var[0]) + "\n"
        for i in range(amount - 1):
            string_function += patern_string % (f[i + 1], var[i], var[i + 1])
            string_function += "\n"
        string_function += "1, при x > " + str(var[amount - 1])

        self.ui.functionEdit.setText(string_function)


    def setCharacteristic(self):
        midX = "{:01.8}".format(self.statistic.average_sample)
        d = "{:01.8}".format(self.statistic.dispersion)
        cigma = "{:01.8}".format(self.statistic.deviation)
        s = "{:01.8}".format(self.statistic.corrected_deviation)

        self.ui.middleXEdit.setText(midX)
        self.ui.dispersionEdit.setText(d)
        self.ui.cigmaEdit.setText(cigma)
        self.ui.sEdit.setText(s)

    def plotDistributionFunction(self, variationSeries : list, function : list):
        amount = len(variationSeries)
        
        self.ui.graphWidget.setXRange(variationSeries[0], variationSeries[amount - 1])
        self.ui.graphWidget.setYRange(0, 1)
        self.ui.graphWidget.setTitle("Эмпирическая функция распределения", color=(0, 0, 0), size="15pt")
        self.ui.graphWidget.setLabel('left', "F*(x)", **self.style1)
        self.ui.graphWidget.setLabel('bottom', "x", **self.style1)

        for i in range(amount - 1):
            xi = [variationSeries[i], variationSeries[i + 1]]
            yi = [function[i + 1], function[i + 1]]
            self.ui.graphWidget.plot(xi, yi, pen=self.pen)

        self.ui.graphWidget.plot([-100 * variationSeries[amount - 1], variationSeries[0]], [0, 0], pen=self.pen)    
        self.ui.graphWidget.plot([variationSeries[amount - 1], 100 * variationSeries[amount - 1]], [1, 1], pen=self.pen)

        for i in range(amount):
            xi = [variationSeries[i], variationSeries[i]]
            yi = [function[i + 1], function[i + 1]]
            self.ui.graphWidget.plot(xi, yi, symbol='t3', symbolSize=15, symbolBrush='r')

    
    def plotPoligon(self, variationSeries : list, periodicity : list, type : PoligonType):
        symbols = ["n", "w"]
        texts = ["частоты", "относительной частоты"]

        symbol = symbols[type.value]
        text = texts[type.value]

        self.ui.graphWidget.setXRange(variationSeries[0], variationSeries[len(variationSeries) - 1])
        self.ui.graphWidget.setYRange(min(periodicity), max(periodicity))
        self.ui.graphWidget.setTitle("Полигон " + text, color=(0, 0, 0), size="15pt")
        self.ui.graphWidget.setLabel('left', symbol + "(x)", **self.style1)
        self.ui.graphWidget.setLabel('bottom', "x", **self.style1)
                
        self.ui.graphWidget.plot(variationSeries, periodicity, pen=self.pen, symbol='d', symbolSize=15, symbolBrush='r')

    
    
def main():
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()