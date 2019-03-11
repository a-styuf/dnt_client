import time
import mko
import numpy
import copy
from ctypes import c_int8, c_int16


class DatControl:
    def __init__(self):
        # mko  класс для общения с ДНТ
        self.mko = mko.TA1()
        self.mko.init()
        self.dnt_mko_connect = 0
        self.dnt_mko_address = 19
        # кадр с данными для чтения
        self.row_read_frame = []
        self.row_write_frame = []
        self.dnt_read_data_name = ["Время, с",
                                   "I ДНТ, кв.АЦП",
                                   "I ДНТ, А",
                                   "T, °С",
                                   "U сетки, В",
                                   "КУ",
                                   "АЦП КУ1, кв.АЦП",
                                   "АЦП КУ10, кв.АЦП",
                                   "АЦП КУ100, кв.АЦП",
                                   "АЦП КУ1000, кв.АЦП",
                                   "Смещение КУ1, кв.АЦП",
                                   "Смещение КУ10, кв.АЦП",
                                   "Смещение КУ100, кв.АЦП",
                                   "Смещение КУ1000, кв.АЦП",
                                   "Ток КУ1, кв.АЦП",
                                   "Ток КУ10, кв.АЦП",
                                   "Ток КУ100, кв.АЦП",
                                   "Ток КУ1000, кв.АЦП",
                                   ]
        self.dnt_read_data = ["0" for i in range(len(self.dnt_read_data_name))]
        self.graph_data = [[self.dnt_read_data_name[i], []] for i in range(len(self.dnt_read_data_name))]
        self.dnt_status = 0x00
        self.dnt_current_adc = 0x00
        #
        self.graph_max_len = 7200
        # калибровочные коэффициенты Ток
        self.cal_a = [3.1884E-11, 3.1424E-12, 3.1724E-13, 3.1400E-14]
        self.cal_b = [-1.7906E-11, -6.7753E-12, 1.1017E-11, 8.3339E-12]
        pass

    def read_gen_data(self):
        self.row_read_frame = self.mko.ReadFromRT(self.dnt_mko_address, 30, 32)
        read_frame_str = ""
        for i in range(32):
            read_frame_str += ("%04X " % self.row_read_frame[i])
        print(read_frame_str)
        if self.row_read_frame[0] == 0x0FF1 and self.row_read_frame[1] == 0x4820:
            self.dnt_status = (self.row_read_frame[13] & 0x000F)
            self.dnt_current_adc = c_int16(self.row_read_frame[2]).value
            # данные в лист с данными ДНТ
            self.dnt_read_data[0] = "%.1f" % time.clock()

            self.dnt_read_data[1] = "%d" % self.dnt_current_adc
            self.dnt_read_data[2] = "%.2E" % (self.cal_a[self.dnt_status] * self.dnt_current_adc +
                                              self.cal_b[self.dnt_status])  # todo: проверить на знак
            self.dnt_read_data[3] = "%.2f" % (c_int16(self.row_read_frame[3]).value / 256)
            self.dnt_read_data[4] = "%.2f" % (self.row_read_frame[4] / 256)
            self.dnt_read_data[5] = "%d" % (10 ** self.dnt_status)
            #
            self.dnt_read_data[6] = "%d" % c_int16(self.row_read_frame[5]).value
            self.dnt_read_data[7] = "%d" % c_int16(self.row_read_frame[6]).value
            self.dnt_read_data[8] = "%d" % c_int16(self.row_read_frame[7]).value
            self.dnt_read_data[9] = "%d" % c_int16(self.row_read_frame[8]).value

            self.dnt_read_data[10] = "%d" % c_int16(self.row_read_frame[9]).value
            self.dnt_read_data[11] = "%d" % c_int16(self.row_read_frame[10]).value
            self.dnt_read_data[12] = "%d" % c_int16(self.row_read_frame[11]).value
            self.dnt_read_data[13] = "%d" % c_int16(self.row_read_frame[12]).value

            self.dnt_read_data[14] = "%d" % (c_int16(self.row_read_frame[5]).value - c_int16(self.row_read_frame[9]).value)
            self.dnt_read_data[15] = "%d" % (c_int16(self.row_read_frame[6]).value - c_int16(self.row_read_frame[10]).value)
            self.dnt_read_data[16] = "%d" % (c_int16(self.row_read_frame[7]).value - c_int16(self.row_read_frame[11]).value)
            self.dnt_read_data[17] = "%d" % (c_int16(self.row_read_frame[8]).value - c_int16(self.row_read_frame[12]).value)
        pass

    def create_graph_data(self):
        # добавляем данные
        for num, var in enumerate(self.graph_data):
            var[1].append(float(self.dnt_read_data[num]))
            # ограничивываем длину данных для отрисовки
            while 1:
                if len(var[1]) > self.graph_max_len:
                    var[1] = var[1][1:]
                else:
                    break
        pass

    def reset_graph_data(self):
        self.graph_data = [[self.dnt_read_data_name[i], []] for i in range(len(self.dnt_read_data_name))]
        pass

    def set_param(self, meas_time_s=1, meas_interval_ms=5, dead_time_ms=100):
        self.row_write_frame = [0xFAFA for i in range(32)]
        self.row_write_frame[0] = 0x0FF1
        self.row_write_frame[1] = 0x4821
        self.row_write_frame[2] = value_from_bound(meas_time_s, 1, 20) & 0xFFFF
        self.row_write_frame[3] = value_from_bound(meas_interval_ms, 4, 20) & 0xFFFF
        self.row_write_frame[4] = value_from_bound(dead_time_ms, 10, 200) & 0xFFFF
        self.row_write_frame[5] = 0x0000
        self.row_write_frame[6] = 0x0000
        self.row_write_frame[7] = 0x0000
        print(self.row_write_frame)
        aw = self.mko.SendToRT(self.dnt_mko_address, 29, self.row_write_frame, 32)
        print("%04X" % aw)
        pass


def value_from_bound(val, val_min, val_max):
    return max(val_min, min(val_max, val))
