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
        self.setWindowTitle("ДНТ Клиент: ДНТ зав.№ не выбран")
        # класс для управления ДНТ
        self.dnt = dnt_data.DateControl()
        self.mkoReconnectPButt.clicked.connect(self.dnt.mko.init)
        # загузка/сохранение конфигурации ПО
        self.used_cfg_file = ""
        self.load_main_cfg()
        # загузка/сохранение конфигурации ДНТ
        self.cfgDNTConfigOpenQAction.triggered.connect(self.load_dnt_cfg)
        self.cfgDNTConfigSaveQAction.triggered.connect(self.save_dnt_cfg)
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
        self.readDataTWidget.setHorizontalHeaderLabels(self.dnt.dnt_label_statistics_column)
        for column in range(self.readDataTWidget.columnCount()):
            if column == 0:
                self.readDataTWidget.setColumnWidth(column, 125)
            else:
                self.readDataTWidget.setColumnWidth(column, 80)
        self.DataUpdateTimer = QtCore.QTimer()
        self.DataUpdateTimer.timeout.connect(self.update_ui)
        self.DataUpdateTimer.start(1000)

        # управление ДНТ параметров
        self.setParamPButton.clicked.connect(self.set_parameters)
        self.setParamPButton.setStyleSheet("background-color: " + "lightsteelblue")
        self.getParamPButton.clicked.connect(self.get_parameters)
        self.getParamPButton.setStyleSheet("background-color: " + "lemonchiffon")

        self.singleMeasurementTimer = QtCore.QTimer()
        self.singleMeasurementTimer.timeout.connect(self.single_measurement_finish)
        self.test_count = 0
        self.singleMeasurementPButton.clicked.connect(self.start_single_measurement)
        self.singleMeasurementPButton.setStyleSheet("background-color: " + "lightgreen")

        self.cycleMeasurementPButton.clicked.connect(self.start_cycle_measurement)
        self.cycleMeasurementPButton.setStyleSheet("background-color: " + "lightgreen")

        # управление калибровками
        self.calibrationTWidget.cellChanged.connect(self.update_calibration_coeff_from_table)

        # логи
        self.log_file = None
        self.log_str = ""
        self.recreate_log_files()
        self.dntLogRestartPButt.clicked.connect(self.recreate_log_files)

        # осциллограммы
        self.osc_button_sender = None
        self.readOscSignKU1PButt.clicked.connect(lambda: self.read_osc(osc_ku=0, osc_mode="adc"))
        self.readOscSignKU10PButt.clicked.connect(lambda: self.read_osc(osc_ku=1, osc_mode="adc"))
        self.readOscSignKU100PButt.clicked.connect(lambda: self.read_osc(osc_ku=2, osc_mode="adc"))
        self.readOscSignKU1000PButt.clicked.connect(lambda: self.read_osc(osc_ku=3, osc_mode="adc"))
        self.readOscZeroKU1PButt.clicked.connect(lambda: self.read_osc(osc_ku=0, osc_mode="zero"))
        self.readOscZeroKU10PButt.clicked.connect(lambda: self.read_osc(osc_ku=1, osc_mode="zero"))
        self.readOscZeroKU100PButt.clicked.connect(lambda: self.read_osc(osc_ku=2, osc_mode="zero"))
        self.readOscZeroKU1000PButt.clicked.connect(lambda: self.read_osc(osc_ku=3, osc_mode="zero"))
        self.clearOscPButt.clicked.connect(self.stop_osc_mode)
        self.clearOscPButt.setStyleSheet("background-color: " + "lightgray")

    def read_data_cycle_body(self):
        period = self.cycleReadDataSBox.value()
        self.readDataCycleTimer.setInterval(period * 1000)
        #
        self.dnt.read_gen_data()
        pass

    def update_ui(self):
        try:
            # заоплнение таблицы c данными
            for row in range(len(self.dnt.dnt_read_data_name)):
                try:
                    table_item = QtWidgets.QTableWidgetItem(self.dnt.dnt_read_data_name[row])
                    self.readDataTWidget.setItem(row, 0, table_item)
                    for column in range(1, len(self.dnt.dnt_label_statistics_column)):
                        table_item = QtWidgets.QTableWidgetItem(self.dnt.dnt_read_data[row][column-1])
                        self.readDataTWidget.setItem(row, column, table_item)
                except IndexError as error:
                    print(error)
            # отрисовка графика
            # self.dnt.create_graph_data()
            self.dnt_graph_layot.plot_dnt_current(self.dnt.graph_data)
            # логи
            log_str_tmp = ";".join(self.dnt.dnt_read_data[0]).replace(".", ",")
            if self.log_str == log_str_tmp:
                pass
            else:
                self.log_str = log_str_tmp
                self.log_file.write(self.log_str + "\n")
            #
            self.dnt.mko.init()
        except Exception as error:
            print(error)

    def set_parameters(self):
        meas_time_s = self.measurementTimeSBox.value()
        dead_time_ms = self.deadTimeSBOX.value()
        self.dnt.set_param(meas_time_s=meas_time_s, dead_time_ms=dead_time_ms)
        self.deadTimeSBOX.setStyleSheet("background-color: " + "lightsteelblue")
        self.measurementTimeSBox.setStyleSheet("background-color: " + "lightsteelblue")
        pass

    def get_parameters(self):
        self.dnt.read_parameters_data()
        self.measurementTimeSBox.setValue(self.dnt.measurement_time)
        self.measurementTimeSBox.setStyleSheet("background-color: " + "lemonchiffon")
        self.deadTimeSBOX.setValue(self.dnt.dead_time)
        self.deadTimeSBOX.setStyleSheet("background-color: " + "lemonchiffon")
        pass

    def start_single_measurement(self):
        if self.singleMeasurementPButton.isChecked() is True:
            self.dnt.set_param(meas_time_s=self.dnt.measurement_time, dead_time_ms=self.dnt.dead_time, dnt_mode="single")
            # было бы отлично добавить таймер или поток с проверкой окончания единичного измерения с изменением цвета
            timeout = 2 if self.dnt.measurement_time < 2 else self.dnt.measurement_time
            self.singleMeasurementTimer.singleShot(1000*timeout, self.single_measurement_finish)
        else:
            pass
        pass

    def single_measurement_finish(self):
        self.singleMeasurementPButton.setChecked(False)
        self.cycleMeasurementPButton.setChecked(False)
        pass

    def start_cycle_measurement(self):
        if self.cycleMeasurementPButton.isChecked() is False:
            self.dnt.set_param(meas_time_s=self.dnt.measurement_time, dead_time_ms=self.dnt.dead_time, dnt_mode="none")
        elif self.cycleMeasurementPButton.isChecked() is True:
            self.dnt.set_param(meas_time_s=self.dnt.measurement_time, dead_time_ms=self.dnt.dead_time, dnt_mode="cycle")
        pass

    def update_calibration_coeff_from_table(self, row, column):
        # обновляем данные с калибровкой для измененной клетки
        try:
            self.dnt.cal_a[row] = float(self.calibrationTWidget.item(row, column).text())
            self.dnt.cal_b[row] = float(self.calibrationTWidget.item(row, column).text())
        except ValueError:
            table_item = QtWidgets.QTableWidgetItem("%.3E" % self.dnt.cal_a[row])
            self.calibrationTWidget.setItem(row, column, table_item)
            table_item = QtWidgets.QTableWidgetItem("%.3E" % self.dnt.cal_b[row])
            self.calibrationTWidget.setItem(row, column, table_item)
            pass
        except AttributeError:
            pass

    def update_calibration_table(self):
        for row in range(len(self.dnt.cal_a)):
            try:
                if float(self.calibrationTWidget.item(row, 0).text()) != self.dnt.cal_a[row]:
                    table_item = QtWidgets.QTableWidgetItem("%.3E" % self.dnt.cal_a[row])
                    self.calibrationTWidget.setItem(row, 0, table_item)
                if float(self.calibrationTWidget.item(row, 1).text()) != self.dnt.cal_b[row]:
                    table_item = QtWidgets.QTableWidgetItem("%.3E" % self.dnt.cal_b[row])
                    self.calibrationTWidget.setItem(row, 1, table_item)
            except IndexError:
                pass
            except AttributeError:  # таблица еще не создана
                pass

    def read_osc(self, osc_ku=0, osc_mode="adc"):
        self.osc_button_sender = self.sender()
        self.clearOscPButt.setStyleSheet("background-color: " + "lightcoral")
        self.sender().setDisabled(True)
        self.dnt.start_osc(osc_ku=osc_ku, osc_mode=osc_mode)
        self.DataUpdateTimer.stop()
        for i in range(10):
            time.sleep(1)
            if self.dnt.check_osc() == 0:
                self.dnt.read_osc()
                self.dnt_graph_layot.plot_osc_dnt(self.dnt.osc_graph_data, osc_data_type=self.dnt.osc_data_type)
                break
        self.osc_button_sender.setDisabled(False)
        pass

    def stop_osc_mode(self):
        self.DataUpdateTimer.start(1000)
        self.clearOscPButt.setStyleSheet("background-color: " + "lightgray")
        self.dnt.reset_osc_data()


    # Config load/save #
    def load_main_cfg(self):
        file_name = "init.cfg"
        config = configparser.ConfigParser()
        config.read(file_name)
        try:
            self.used_cfg_file = config["Last work parameters"]["last used cfg file"]
            self.load_dnt_cfg_from_file(file_name=self.used_cfg_file)
        except KeyError:
            pass

    def save_main_cfg(self):
        config = configparser.ConfigParser()
        config["Last work parameters"] = {"last used cfg file": self.used_cfg_file}
        try:
            configfile = open("init.cfg", 'w')
            config.write(configfile)
            configfile.close()
        except FileNotFoundError as error:
            print(error)
            pass

        pass

    def load_dnt_cfg(self):
        home_dir = os.getcwd()
        try:
            os.mkdir(home_dir + "\\DNT config")
        except OSError as error:
            print(error)
            pass
        file_name = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          "Открыть файл конфигурации",
                                                          home_dir + "\\DNT config",
                                                          r"config(*.cfg);;All Files(*)")[0]
        self.load_dnt_cfg_from_file(file_name=file_name)
        pass

    def load_dnt_cfg_from_file(self, file_name):
        self.dnt.load_conf_from_file(file_name=file_name)
        self.setWindowTitle("ДНТ Клиент: ДНТ зав.№ %s" % self.dnt.fabrication_number + " " + file_name)
        # заполенение таблицы с калибровкой
        self.update_calibration_table()
        self.used_cfg_file = file_name

    def save_dnt_cfg(self):
        home_dir = os.getcwd()
        try:
            os.mkdir(home_dir + "\\DNT config")
        except OSError:
            pass
        file_name = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          "Сохранить файл конфигурации",
                                                          home_dir + "\\DNT config",
                                                          r"config(*.cfg);;All Files(*)")[0]
        self.dnt.save_conf_to_file(file_name=file_name)
        pass

    # LOGs #
    def create_log_file(self, file=None, prefix="", extension=".csv"):
        dir_name = "Logs"
        sub_dir_name = dir_name + "\\" + time.strftime("%Y_%m_%d", time.localtime()) + " Лог"
        sub_sub_dir_name = sub_dir_name + "\\" + time.strftime("%Y_%m_%d %H-%M-%S ",
                                                               time.localtime()) + "Лог"
        try:
            os.makedirs(sub_sub_dir_name)
        except (OSError, AttributeError) as error:
            pass
        try:
            if file:
                file.close()
        except (OSError, NameError, AttributeError) as error:
            pass
        file_name = sub_sub_dir_name + "\\" + time.strftime("%Y_%m_%d %H-%M-%S ",
                                                            time.localtime()) + prefix + " " + extension
        file = open(file_name, 'a')
        return file

    def recreate_log_files(self):
        self.log_file = self.create_log_file(prefix="био_днт", extension=".csv")
        self.log_file.write(";".join(self.dnt.dnt_read_data_name) + "\n")
        pass

    def close_log_file(self, file=None):
        if file:
            try:
                file.close()
            except (OSError, NameError, AttributeError) as error:
                pass
        pass

    #
    def closeEvent(self, event):
        self.close_log_file(file=self.log_file)
        self.save_main_cfg()
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
