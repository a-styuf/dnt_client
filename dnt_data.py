import time
import ta1_mko
import numpy
import copy
from ctypes import c_int8, c_int16
import configparser
import os
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


class DateControl:
    def __init__(self):
        # mko  класс для общения с ДНТ
        self.mko = ta1_mko.Device()
        self.mko.init()
        self.dnt_mko_connect = 0
        # общие параметры ДНТ
        self.mko_address = 19
        self.data_sa = 30
        self.parameters_sa = 29
        self.fabrication_number = u"не выбран"
        self.report = ""  # вывод сырой строки МКО
        # калибровочные коэффициенты
        self.cal_a = [3.1884E-11, 3.1424E-12, 3.1724E-13, 3.1400E-14]
        self.cal_b = [-1.7906E-11, -6.7753E-12, 1.1017E-11, 8.3339E-12]
        # кадр с данными для чтения
        self.row_read_frame = []
        self.row_write_frame = self.row_write_frame = [0xFAFA for i in range(32)]
        self.row_osc_data = 0
        self.dnt_label_statistics_column = ("Имя", "Знач", "Средн", "Стд.откл", "Макс", "Мин")
        self.dnt_read_data_name = ["Время, с",  # 0
                                   "Время ДНТ, с",  # 1
                                   "Номер кадра, шт.",  # 2
                                   "I ДНТ, А",  # 3
                                   "I ДНТ, кв.АЦП",  # 4
                                   "Сигнал, кв.АЦП",  # 5
                                   "Ноль, кв.АЦП",  # 6
                                   "T, °С",  # 7
                                   "U сетки, В",  # 8
                                   "КУ",  # 9
                                   ]
        self.template = ["0" for i in range(len(self.dnt_label_statistics_column) - 1)]  # -1 - отбрасываем имя
        self.dnt_read_data = [copy.deepcopy(self.template) for i in range(len(self.dnt_read_data_name))]
        self.graph_data = [[self.dnt_read_data_name[i], []] for i in range(len(self.dnt_read_data_name))]
        #
        self.dnt_osc_data_name = ["Время, с",
                                  "АЦП КУ1, кв.АЦП",
                                  "АЦП КУ10, кв.АЦП",
                                  "АЦП КУ100, кв.АЦП",
                                  "АЦП КУ1000, кв.АЦП",
                                  "Нуль КУ1, кв.АЦП",
                                  "Нуль КУ10, кв.АЦП",
                                  "Нуль КУ100, кв.АЦП",
                                  "Нуль КУ1000, кв.АЦП",
                                  ]
        self.dnt_osc_data = ["0" for i in range(len(self.dnt_osc_data_name))]
        self.osc_graph_data = []
        self.reset_osc_data()
        self.osc_data_type = 0
        #
        self.ku = 0x00
        self.dnt_current_adc = 0x00
        self.measurement_time = 1
        self.dead_time = 100
        self.dnt_mode = 0
        #
        self.graph_max_len = 7200
        pass

    def save_conf_to_file(self, file_name="dnt_default.cfg"):
        home_dir = os.getcwd()
        config = configparser.ConfigParser()
        config = self.get_cfg(config)
        try:
            os.mkdir(home_dir + "\\DNT config")
        except OSError:
            pass
        try:
            configfile = open(file_name, 'w')
            config.write(configfile)
            configfile.close()
        except FileNotFoundError as error:
            print(error)
            pass

    def load_conf_from_file(self, file_name="dnt_default.cfg"):
        config = configparser.ConfigParser()
        home_dir = os.getcwd()
        try:
            os.mkdir(home_dir + "\\DNT config")
        except OSError as error:
            print(error)
            pass
        config.read(file_name)
        self.set_cfg(config)
        pass

    def get_cfg(self, config):
        for i in range(4):
            config["Current calibration KU = %d" % i] = {"a": "%.3E" % self.cal_a[i],
                                                         "b": "%.3E" % self.cal_b[i]}
        config["General parameters"] = {"fabrication number": "%s" % self.fabrication_number,
                                        "mko address": "%d" % self.mko_address}
        return config

    def set_cfg(self, config):
        try:
            for i in range(4):
                self.cal_a[i] = float(config["Current calibration KU = %d" % i]["a"])
                self.cal_b[i] = float(config["Current calibration KU = %d" % i]["b"])
            self.fabrication_number = config["General parameters"]["fabrication number"]
            self.mko_address = int(config["General parameters"]["mko address"])
        except KeyError as error:
            print(error, "DNT config file not found. Use last value")
        pass

    def check_frame_definer(self, frame_definer, frame_type=0):
        try:
            fabrication_number_int = int(self.fabrication_number)
        except ValueError as error:
            # print(error, "")
            fabrication_number_int = 0
        valid_frame_definer = calc_frame_definer(frame_mode=0x01, device_type=0x02,
                                                 fabrication_number=fabrication_number_int, frame_type=frame_type)
        if fabrication_number_int == 0:
            if (frame_definer & 0xFC07) == (valid_frame_definer & 0xFC07):
                return True
        else:
            if frame_definer == valid_frame_definer:
                return True
            else:
                return False

    def set_frame_definer(self, frame_type=0):
        try:
            fabrication_number_int = int(self.fabrication_number)
        except ValueError as error:
            # print(error, "")
            fabrication_number_int = 0
        return calc_frame_definer(frame_mode=0x01, device_type=0x02,
                                  fabrication_number=fabrication_number_int, frame_type=frame_type)

    def read_gen_data(self):
        self.row_read_frame = self.mko.read_from_rt(self.mko_address, self.data_sa, 32)
        self.report = list_to_str(self.row_read_frame)
        print(self.report)
        if self.row_read_frame[0] == 0x0FF1 and self.check_frame_definer(self.row_read_frame[1], frame_type=0):

            # данные в лист с данными ДНТ
            self.dnt_read_data[0][0] = "%.1f" % time.perf_counter()

            self.dnt_read_data[1][0] = "%d" % ((c_int16(self.row_read_frame[3]).value << 16) +
                                               c_int16(self.row_read_frame[4]).value)
            self.dnt_read_data[2][0] = "%d" % c_int16(self.row_read_frame[2]).value

            self.dnt_current_adc = c_int16(self.row_read_frame[5]).value
            self.dnt_read_data[4][0] = "%d" % self.dnt_current_adc

            self.dnt_read_data[5][0] = "%d" % c_int16(self.row_read_frame[6]).value
            self.dnt_read_data[6][0] = "%d" % c_int16(self.row_read_frame[7]).value
            self.dnt_read_data[7][0] = "%.1f" % (c_int16(self.row_read_frame[8]).value / 256)
            self.dnt_read_data[8][0] = "%.1f" % (c_int16(self.row_read_frame[9]).value / 256)

            self.ku = c_int16(self.row_read_frame[10]).value & 0x03
            self.dnt_read_data[9][0] = "%d" % (10 ** self.ku)

            self.dnt_read_data[3][0] = "%.3E" % (self.cal_a[self.ku] * self.dnt_current_adc + self.cal_b[self.ku])
            self.create_graph_data()
            self.calc_statistic_data()
        pass

    def read_parameters_data(self):
        self.row_read_frame = self.mko.read_from_rt(self.mko_address, self.parameters_sa, 32)
        self.report = list_to_str(self.row_read_frame)
        print(self.report)
        if self.row_read_frame[0] == 0x0FF1 and self.check_frame_definer(self.row_read_frame[1], frame_type=1):
            # данные в лист с данными ДНТ
            self.dnt_mode = self.row_read_frame[6] & 0xFF
            self.measurement_time = self.row_read_frame[2]
            self.dead_time = self.row_read_frame[3]
            return 1
        return -1

    def create_graph_data(self):
        # добавляем данные
        for num, var in enumerate(self.graph_data):
            var[1].append(float(self.dnt_read_data[num][0]))
            # ограничивываем длину данных для отрисовки
            while 1:
                if len(var[1]) > self.graph_max_len:
                    var[1] = var[1][1:]
                else:
                    break
        pass

    def calc_statistic_data(self):
        try:
            for i in range(len(self.dnt_read_data_name)):
                self.dnt_read_data[i][1] = "%.3E" % numpy.mean(self.graph_data[i][1])
                self.dnt_read_data[i][2] = "%.3E" % numpy.std(self.graph_data[i][1])
                self.dnt_read_data[i][3] = "%.3E" % max(self.graph_data[i][1])
                self.dnt_read_data[i][4] = "%.3E" % min(self.graph_data[i][1])
        except RuntimeWarning as error:
            print("calc_statistic_data" + error)

    def reset_graph_data(self):
        self.graph_data = [[self.dnt_read_data_name[i], []] for i in range(len(self.dnt_read_data_name))]
        pass

    def set_param(self, meas_time_s=1, dead_time_ms=100, dnt_mode="none", osc_ku=0, osc_mode="adc"):
        # читаем параметры dnt для того, что бы не затереть старые
        self.read_parameters_data()
        print(self.dnt_mode)
        #
        self.measurement_time = meas_time_s
        self.dead_time = dead_time_ms
        self.row_write_frame = [0xFAFA for i in range(32)]
        self.row_write_frame[0] = 0x0FF1
        self.row_write_frame[1] = self.set_frame_definer(frame_type=1)
        self.row_write_frame[2] = value_from_bound(self.measurement_time, 1, 20) & 0xFFFF
        self.row_write_frame[3] = value_from_bound(self.dead_time, 10, 200) & 0xFFFF
        self.row_write_frame[4] = 0x0000 if osc_mode == "adc" else 0x0001
        self.row_write_frame[5] = osc_ku
        if "none" in dnt_mode:
            mode_uint16 = 0x00
        elif "cycle_on" in dnt_mode:
            mode_uint16 = self.dnt_mode | 0x04
        elif "cycle_off" in dnt_mode:
            mode_uint16 = self.dnt_mode & (~0x04)
        elif "single" in dnt_mode:
            mode_uint16 = 0x02
        elif "osc" in dnt_mode:
            mode_uint16 = self.dnt_mode | 0x01
        elif "const_on" in dnt_mode:
            mode_uint16 = self.dnt_mode | 0x10
        elif "const_off" in dnt_mode:
            mode_uint16 = self.dnt_mode & (~0x10)
        else:
            mode_uint16 = 0x00
        self.row_write_frame[6] = mode_uint16
        #
        self.report = list_to_str(self.row_write_frame)
        print(mode_uint16)
        print(self.report)
        #
        aw = self.mko.send_to_rt(self.mko_address, self.parameters_sa, self.row_write_frame, 32)
        pass

    def start_osc(self, osc_ku=0, osc_mode="adc"):  # ku: 0-1, 1-10, 2-100, 3-1000
        self.set_param(osc_ku=osc_ku, dnt_mode="osc", osc_mode=osc_mode)
        osc_mode_int = 0x0000 if osc_mode == "adc" else 0x0001
        self.osc_data_type = osc_mode_int*4 + osc_ku + 1
        pass

    def check_osc(self):
        state = self.read_parameters_data()
        if state == 1:
            if self.dnt_mode & 0x01 != 0x0000:
                self.report = "wait"
                return 1
            else:
                self.report = "ready"
                return 0
        return state

    def read_osc(self):
        self.row_osc_data = []
        for i in range(16):
            self.row_osc_data.extend(self.mko.read_from_rt(self.mko_address, i + 1, 32))
            # print(list_to_str(self.row_osc_data[-32:]))
        self.osc_graph_data[self.osc_data_type][1] = []
        for num, var in enumerate(self.row_osc_data):
            self.osc_graph_data[self.osc_data_type][1].append(var)
            pass

    def reset_osc_data(self):
        self.osc_graph_data = [[self.dnt_osc_data_name[i], []] for i in range(len(self.dnt_osc_data_name))]
        self.osc_graph_data[0][1] = [num * (20.5 * 1E-3 / 512) for num in range(16 * 32)]
        pass


def value_from_bound(val, val_min, val_max):
    return max(val_min, min(val_max, val))


def list_to_str(input_list):
    return_str = " ".join(["%04X " % var for var in input_list])
    return return_str


def calc_frame_definer(frame_mode=0x01, device_type=0x02, fabrication_number=0x01, frame_type=0x00):
    frame_definer = ((frame_mode & 0x3) << 14) + \
                    ((device_type & 0xF) << 10) + \
                    ((fabrication_number & 0x7F) << 3) + \
                    ((frame_type & 0x7) << 0)
    return frame_definer
