# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/qingchu/fun/Smarthome/code/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1054, 644)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setGeometry(QtCore.QRect(10, 50, 651, 321))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.graphWidget_temp = PlotWidget(self.splitter)
        self.graphWidget_temp.setEnabled(True)
        self.graphWidget_temp.setObjectName("graphWidget_temp")
        self.graphWidget_humi = PlotWidget(self.splitter)
        self.graphWidget_humi.setEnabled(True)
        self.graphWidget_humi.setObjectName("graphWidget_humi")
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(800, 80, 91, 201))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_read = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_read.setObjectName("pushButton_read")
        self.verticalLayout.addWidget(self.pushButton_read)
        self.pushButton_record = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_record.setObjectName("pushButton_record")
        self.verticalLayout.addWidget(self.pushButton_record)
        self.pushButton_stop = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.verticalLayout.addWidget(self.pushButton_stop)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My smart home"))
        self.pushButton_read.setText(_translate("MainWindow", "Read"))
        self.pushButton_record.setText(_translate("MainWindow", "Record"))
        self.pushButton_stop.setText(_translate("MainWindow", "stop"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
