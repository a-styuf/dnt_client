# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_win.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1287, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.controlGBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlGBox.sizePolicy().hasHeightForWidth())
        self.controlGBox.setSizePolicy(sizePolicy)
        self.controlGBox.setMinimumSize(QtCore.QSize(320, 0))
        self.controlGBox.setObjectName("controlGBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.controlGBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.getParamPButton = QtWidgets.QPushButton(self.controlGBox)
        self.getParamPButton.setObjectName("getParamPButton")
        self.gridLayout_2.addWidget(self.getParamPButton, 1, 1, 1, 1)
        self.setParamPButton = QtWidgets.QPushButton(self.controlGBox)
        self.setParamPButton.setObjectName("setParamPButton")
        self.gridLayout_2.addWidget(self.setParamPButton, 1, 0, 1, 1)
        self.paramTWidget = QtWidgets.QTableWidget(self.controlGBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paramTWidget.sizePolicy().hasHeightForWidth())
        self.paramTWidget.setSizePolicy(sizePolicy)
        self.paramTWidget.setMinimumSize(QtCore.QSize(300, 350))
        self.paramTWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.paramTWidget.setRowCount(3)
        self.paramTWidget.setColumnCount(2)
        self.paramTWidget.setObjectName("paramTWidget")
        item = QtWidgets.QTableWidgetItem()
        self.paramTWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.paramTWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.paramTWidget.setItem(2, 1, item)
        self.paramTWidget.horizontalHeader().setDefaultSectionSize(140)
        self.paramTWidget.verticalHeader().setDefaultSectionSize(35)
        self.gridLayout_2.addWidget(self.paramTWidget, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 2)
        self.oscLabel = QtWidgets.QLabel(self.controlGBox)
        self.oscLabel.setObjectName("oscLabel")
        self.gridLayout_2.addWidget(self.oscLabel, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.controlGBox, 0, 0, 1, 1)
        self.dataGBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataGBox.sizePolicy().hasHeightForWidth())
        self.dataGBox.setSizePolicy(sizePolicy)
        self.dataGBox.setMinimumSize(QtCore.QSize(350, 0))
        self.dataGBox.setObjectName("dataGBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.dataGBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.cycleReadDataPButt = QtWidgets.QPushButton(self.dataGBox)
        self.cycleReadDataPButt.setMinimumSize(QtCore.QSize(200, 0))
        self.cycleReadDataPButt.setObjectName("cycleReadDataPButt")
        self.gridLayout_3.addWidget(self.cycleReadDataPButt, 3, 0, 1, 1)
        self.readDataPButt = QtWidgets.QPushButton(self.dataGBox)
        self.readDataPButt.setObjectName("readDataPButt")
        self.gridLayout_3.addWidget(self.readDataPButt, 1, 0, 1, 2)
        self.cycleReadDataSBox = QtWidgets.QSpinBox(self.dataGBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cycleReadDataSBox.sizePolicy().hasHeightForWidth())
        self.cycleReadDataSBox.setSizePolicy(sizePolicy)
        self.cycleReadDataSBox.setMinimumSize(QtCore.QSize(0, 30))
        self.cycleReadDataSBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cycleReadDataSBox.setMinimum(1)
        self.cycleReadDataSBox.setMaximum(3600)
        self.cycleReadDataSBox.setObjectName("cycleReadDataSBox")
        self.gridLayout_3.addWidget(self.cycleReadDataSBox, 3, 1, 1, 1)
        self.readDataTWidget = QtWidgets.QTableWidget(self.dataGBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readDataTWidget.sizePolicy().hasHeightForWidth())
        self.readDataTWidget.setSizePolicy(sizePolicy)
        self.readDataTWidget.setMinimumSize(QtCore.QSize(300, 550))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.readDataTWidget.setFont(font)
        self.readDataTWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.readDataTWidget.setRowCount(50)
        self.readDataTWidget.setColumnCount(2)
        self.readDataTWidget.setObjectName("readDataTWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(7)
        item.setFont(font)
        self.readDataTWidget.setItem(0, 0, item)
        self.readDataTWidget.horizontalHeader().setDefaultSectionSize(150)
        self.readDataTWidget.horizontalHeader().setMinimumSectionSize(150)
        self.readDataTWidget.verticalHeader().setDefaultSectionSize(30)
        self.readDataTWidget.verticalHeader().setMinimumSectionSize(25)
        self.gridLayout_3.addWidget(self.readDataTWidget, 0, 0, 1, 2)
        self.stopCyclePButt = QtWidgets.QPushButton(self.dataGBox)
        self.stopCyclePButt.setObjectName("stopCyclePButt")
        self.gridLayout_3.addWidget(self.stopCyclePButt, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.dataGBox, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.mkoReconnectPButt = QtWidgets.QPushButton(self.centralwidget)
        self.mkoReconnectPButt.setObjectName("mkoReconnectPButt")
        self.horizontalLayout.addWidget(self.mkoReconnectPButt)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(5, -1, 5, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.dntGraphResetPButt = QtWidgets.QPushButton(self.centralwidget)
        self.dntGraphResetPButt.setObjectName("dntGraphResetPButt")
        self.gridLayout_4.addWidget(self.dntGraphResetPButt, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 1, 0, 1, 1)
        self.dntDataGView = QtWidgets.QGraphicsView(self.centralwidget)
        self.dntDataGView.setObjectName("dntDataGView")
        self.gridLayout_4.addWidget(self.dntDataGView, 0, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_4, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ДНТ Клиент"))
        self.controlGBox.setTitle(_translate("MainWindow", "Управление"))
        self.getParamPButton.setText(_translate("MainWindow", "Прочитать"))
        self.setParamPButton.setText(_translate("MainWindow", "Установить"))
        item = self.paramTWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Имя"))
        item = self.paramTWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Значение"))
        __sortingEnabled = self.paramTWidget.isSortingEnabled()
        self.paramTWidget.setSortingEnabled(False)
        item = self.paramTWidget.item(0, 0)
        item.setText(_translate("MainWindow", "Время измерения, с"))
        item = self.paramTWidget.item(0, 1)
        item.setText(_translate("MainWindow", "1"))
        item = self.paramTWidget.item(1, 0)
        item.setText(_translate("MainWindow", "Интервал АЦП, мс"))
        item = self.paramTWidget.item(1, 1)
        item.setText(_translate("MainWindow", "5"))
        item = self.paramTWidget.item(2, 0)
        item.setText(_translate("MainWindow", "Мертвое время, мс"))
        item = self.paramTWidget.item(2, 1)
        item.setText(_translate("MainWindow", "100"))
        self.paramTWidget.setSortingEnabled(__sortingEnabled)
        self.oscLabel.setText(_translate("MainWindow", "Осциллограмма"))
        self.dataGBox.setTitle(_translate("MainWindow", "Опрос"))
        self.cycleReadDataPButt.setText(_translate("MainWindow", "Циклическое чтение"))
        self.readDataPButt.setText(_translate("MainWindow", "Чтение"))
        __sortingEnabled = self.readDataTWidget.isSortingEnabled()
        self.readDataTWidget.setSortingEnabled(False)
        self.readDataTWidget.setSortingEnabled(__sortingEnabled)
        self.stopCyclePButt.setText(_translate("MainWindow", "Остановить циклическое чтение"))
        self.mkoReconnectPButt.setText(_translate("MainWindow", "Переподключение МКО"))
        self.dntGraphResetPButt.setText(_translate("MainWindow", "Перезапуск графика"))
