# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1569, 904)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(790, 250, 721, 601))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout.addWidget(self.calendarWidget)
        self.splitter_3 = QtWidgets.QSplitter(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setHandleWidth(1)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setHandleWidth(1)
        self.splitter_2.setObjectName("splitter_2")
        self.CalendarText_d = QtWidgets.QTextBrowser(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.CalendarText_d.sizePolicy().hasHeightForWidth())
        self.CalendarText_d.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.CalendarText_d.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(35)
        self.CalendarText_d.setFont(font)
        self.CalendarText_d.setObjectName("CalendarText_d")
        self.CalendarText_dmy = QtWidgets.QTextBrowser(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.CalendarText_dmy.sizePolicy().hasHeightForWidth())
        self.CalendarText_dmy.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.CalendarText_dmy.setFont(font)
        self.CalendarText_dmy.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CalendarText_dmy.setObjectName("CalendarText_dmy")
        self.listWidget = QtWidgets.QListWidget(self.splitter_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(16)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.listWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(237, 212, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(13)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.listWidget.addItem(item)
        self.horizontalLayout.addWidget(self.splitter_3)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(790, 10, 721, 221))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.photolabel_1 = QtWidgets.QLabel(self.layoutWidget1)
        self.photolabel_1.setText("")
        self.photolabel_1.setObjectName("photolabel_1")
        self.horizontalLayout_3.addWidget(self.photolabel_1)
        self.photolabel_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.photolabel_2.setText("")
        self.photolabel_2.setObjectName("photolabel_2")
        self.horizontalLayout_3.addWidget(self.photolabel_2)
        self.photolabel_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.photolabel_3.setText("")
        self.photolabel_3.setObjectName("photolabel_3")
        self.horizontalLayout_3.addWidget(self.photolabel_3)
        self.photolabel_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.photolabel_4.setText("")
        self.photolabel_4.setObjectName("photolabel_4")
        self.horizontalLayout_3.addWidget(self.photolabel_4)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(230, 600, 254, 27))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_stop = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_2.addWidget(self.pushButton_stop)
        self.pushButton_record = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_record.setObjectName("pushButton_record")
        self.horizontalLayout_2.addWidget(self.pushButton_record)
        self.pushButton_read = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_read.setObjectName("pushButton_read")
        self.horizontalLayout_2.addWidget(self.pushButton_read)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(40, 680, 641, 101))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.photolabel_temp = QtWidgets.QLabel(self.layoutWidget_2)
        self.photolabel_temp.setText("")
        self.photolabel_temp.setObjectName("photolabel_temp")
        self.horizontalLayout_7.addWidget(self.photolabel_temp)
        self.photolabel_humi = QtWidgets.QLabel(self.layoutWidget_2)
        self.photolabel_humi.setText("")
        self.photolabel_humi.setObjectName("photolabel_humi")
        self.horizontalLayout_7.addWidget(self.photolabel_humi)
        self.photolabel_pm25 = QtWidgets.QLabel(self.layoutWidget_2)
        self.photolabel_pm25.setText("")
        self.photolabel_pm25.setObjectName("photolabel_pm25")
        self.horizontalLayout_7.addWidget(self.photolabel_pm25)
        self.photolabel_pm10 = QtWidgets.QLabel(self.layoutWidget_2)
        self.photolabel_pm10.setText("")
        self.photolabel_pm10.setObjectName("photolabel_pm10")
        self.horizontalLayout_7.addWidget(self.photolabel_pm10)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(40, 20, 641, 571))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutWidget4 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(40, 780, 641, 61))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_temp = QtWidgets.QLabel(self.layoutWidget4)
        self.label_temp.setText("")
        self.label_temp.setObjectName("label_temp")
        self.horizontalLayout_5.addWidget(self.label_temp)
        self.label_humi = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_humi.setFont(font)
        self.label_humi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_humi.setText("")
        self.label_humi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_humi.setObjectName("label_humi")
        self.horizontalLayout_5.addWidget(self.label_humi)
        self.label_pm25 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_pm25.setText("")
        self.label_pm25.setObjectName("label_pm25")
        self.horizontalLayout_5.addWidget(self.label_pm25)
        self.label_pm10 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_pm10.setText("")
        self.label_pm10.setObjectName("label_pm10")
        self.horizontalLayout_5.addWidget(self.label_pm10)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 640, 89, 25))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My smart home"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Meeting"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "12:00 PM-1:00 PM\n"
""))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Meeting 2"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "1:00 PM-2:00 PM\n"
""))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_stop.setText(_translate("MainWindow", "stop"))
        self.pushButton_record.setText(_translate("MainWindow", "Record"))
        self.pushButton_read.setText(_translate("MainWindow", "Read"))
        self.pushButton.setText(_translate("MainWindow", "exit"))