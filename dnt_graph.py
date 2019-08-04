# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Layout(QVBoxLayout):
    def __init__(self, root):
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, root)
        # self.addWidget(self.toolbar)
        self.addWidget(self.canvas)

    def plot_dnt_current(self, graph_data):  # graph_data в формате [["Имя1, ед.изм.", [data]], ["Имя2, ед.изм.", [data]]...]
        try:
            # отрисуем график
            self.figure.clear()
            # create an axis
            axes = self.figure.add_subplot(111)
            axes_twinx = axes.twinx()
            # plot data
            time = graph_data[0][1]
            current = graph_data[3][1]
            current_pos_list = []
            current_neg_list = []
            for var in current:
                current_pos = var if var > 1E-12 else 1E-12
                current_neg = -var if var < -1E-12 else 1E-12
                current_pos_list.append(current_pos)
                current_neg_list.append(current_neg)
            axes.plot(time, current_pos_list, line_type_from_index(0), label=u"Ток +, А")
            axes.plot(time, current_neg_list, line_type_from_index(1), label=u"Ток -, А")
            # подсчет статистических данных
            current_pos_mean = float(np.mean(current_pos_list))
            current_neg_mean = float(np.mean(current_neg_list))
            current_pos_std = float(np.std(current_pos_list))
            current_neg_std = float(np.std(current_neg_list))
            #
            data_text = " mean_pos=%.3E; std_pos=%.2E;\n mean_neg=%.3E; std_neg=%.2E;" \
                        % (current_pos_mean, current_pos_std, current_neg_mean, current_neg_std)
            self.figure.text(0.01, 0.95, data_text)
            #
            axes.set_title("График показаний ДНТ")
            axes.set_xlabel("Время, с")
            axes.set_ylim(bottom=1E-12)
            axes.set_yscale("log")
            axes.legend(loc=2)
            axes.grid()
            # refresh canvas
            self.canvas.draw()
        except Exception as error:
            print("plot_dnt_current " + error)
        pass

    def plot_osc_dnt(self, graph_data, osc_data_type=0):
        try:
            # отрисуем график
            self.figure.clear()
            # create an axis
            axes = self.figure.add_subplot(111)
            # plot data
            time = graph_data[0][1]
            read_flag = 0
            for num, var in enumerate(graph_data[1:]):
                if var[1]:
                    read_flag = 1
                    axes.plot(time, var[1], line_type_from_index(num), label=var[0])
            if read_flag:
                axes.set_title("Осциллограмма ДНТ")
                axes.set_xlabel("Время, с")
                axes.legend(loc=0)
                axes.grid()
                # refresh canvas
                self.canvas.draw()
        except Exception as error:
            print(error)


def line_type_from_index(n):
    color_line = ["r", "b", "g", "c", "m", "y", "k"]
    style_line = ["-", "--", "-.", ":"]
    try:
        color = color_line[n % len(color_line)]
        style = style_line[n // len(color_line)]
        return style + color
    except IndexError:
        return "-r"
