import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor, QBrush
import main_win
import time
import configparser
import os
import dnt_data
import dnt_graph


class MainWindow(QtWidgets.QMainWindow, main_win.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле main_win.py
        #
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.setWindowIcon(QtGui.QIcon('main_icon.png'))
        # класс для управления ДНТ
        self.dnt = dnt_data.DatControl()
        self.mkoReconnectPButt.clicked.connect(self.dnt.mko.init)
        # чтение данных
        self.readDataPButt.clicked.connect(self.dnt.read_gen_data)

        self.cycleReadDataPButt.clicked.connect(lambda: self.readDataCycleTimer.start(1000))
        self.stopCyclePButt.clicked.connect(lambda: self.readDataCycleTimer.stop())

        self.readDataCycleTimer = QtCore.QTimer()
        self.readDataCycleTimer.timeout.connect(self.read_data_cycle_body)

        # График показний ДНТ
        self.dnt_graph_layot = dnt_graph.Layout(self.dntDataGView)
        self.dntDataGView.setLayout(self.dnt_graph_layot)
        self.dntGraphResetPButt.clicked.connect(self.dnt.reset_graph_data)

        # обновление gui
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_ui)
        self.DataUpdateTimer.start(1000)

        # запись параметров
        self.setParamPButton.clicked.connect(self.write_parameters)

    def read_data_cycle_body(self):
        period = self.cycleReadDataSBox.value()
        self.readDataCycleTimer.setInterval(period * 1000)
        #
        self.dnt.read_gen_data()
        pass

    def update_ui(self):
        # заоплнение таблицы
        for row in range(len(self.dnt.dnt_read_data_name)):
            try:
                table_item = QtWidgets.QTableWidgetItem(self.dnt.dnt_read_data_name[row])
                self.readDataTWidget.setItem(row, 0, table_item)
                table_item = QtWidgets.QTableWidgetItem(self.dnt.dnt_read_data[row])
                self.readDataTWidget.setItem(row, 1, table_item)
            except IndexError:
                pass
        # отрисовка графика
        self.dnt.create_graph_data()
        self.dnt_graph_layot.plot_dnt_current(self.dnt.graph_data)

    def write_parameters(self):
        meas_time_s = int(self.paramTWidget.item(0, 1).text())
        meas_interval_ms = int(self.paramTWidget.item(1, 1).text())
        dead_time_ms = int(self.paramTWidget.item(2, 1).text())
        self.dnt.set_param(meas_time_s=meas_time_s, meas_interval_ms=meas_interval_ms, dead_time_ms=dead_time_ms)
        pass

    def closeEvent(self, event):
        self.close()
        pass


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # os.environ["QT_SCALE_FACTOR"] = "1.0"
    #
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
