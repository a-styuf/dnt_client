# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


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
            # plot data
            time = graph_data[0][1]
            current = graph_data[2][1]
            axes.plot(time, current, line_type_from_index(0), label=u"Ток, А")
            axes.set_title("График показаний ДНТ")
            axes.set_xlabel("Время, с")
            # axes.set_ylim(bottom=0)
            axes.set_yscale("log")
            axes.legend(loc=0)
            axes.grid()
            # refresh canvas
            self.canvas.draw()
        except Exception as error:
            print(error)
        pass


def line_type_from_index(n):
    color_line = ["b", "r", "g", "c", "m", "y", "k"]
    style_line = ["-", "--", "-.", ":"]
    try:
        color = color_line[n % len(color_line)]
        style = style_line[n // len(color_line)]
        return style + color
    except IndexError:
        return "-r"
