# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, QLocale
from PyQt5.QtWidgets import QMainWindow,QFileDialog
from .Ui_mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, uic, QtGui,  QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import pandas as pd
import csv
import time
import os
import datetime

# from CalendarBackend import CalendarBackend

import pigpio
import libraries.DHT22 as DHT22
import libraries.SDS011 as SDS011
from libraries.CalendarBackend import CalendarBackend
from utils.utils import *

class Sensorreader(QtCore.QThread):
    '''
    The class (thread) to read the DHT22 sensor and SDS011 sensor.
    '''
    
    data_sensor = QtCore.pyqtSignal(tuple)
    is_killed=False
    #dht initalization
    DHT2_PIN = 4
    pi = pigpio.pi()
    dht22 = DHT22.sensor(pi,4)

    #sds011 initalization
    sds011 = SDS011.SDS011("/dev/ttyUSB0", use_query_mode=True)

    def run(self):
        while True:
            if self.is_killed:
                break
            time.sleep( 2 )
            self.dht22.trigger()
            humidity = self.dht22.humidity()/1.0#np.random.rand(1)
            temperature = self.dht22.temperature()/1.0#np.random.rand(1)
            pm25,pm10 = self.sds011.query()

            self.data_sensor.emit((humidity, temperature,pm25,pm10))

    def kill(self):
        self.is_killed=True
    def init_flags(self):
        self.is_killed=False

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M") for value in values]

# class Sensorreader(QtCore.QThread):
#     '''
#     The class (thread) to read the DHT22 sensor.
#     '''
    
#     data_sensor = QtCore.pyqtSignal(tuple)
#     is_killed=False
#     DHT2_PIN = 4

#     def run(self):
#         while True:
#             if self.is_killed:
#                 break
#             time.sleep( 2 )
#             # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
#             humidity = 30 + np.random.rand(1)
#             temperature = 15 + np.random.rand(1)
#             self.data_sensor.emit((humidity[0], temperature[0],4,5))
#     def kill(self):
#         self.is_killed=True
#     def init_flags(self):
#         self.is_killed=False

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None,):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./imgs/icon.jpg'))
        self.bgcolor = self.palette().color(QtGui.QPalette.Window)  # Get the default window background,
        # print(self.bgcolor.getRgb())
        print(self.bgcolor.getRgb()[0:3])

        ##--------HUMIDITY, TEMPERATURE, PM2.5 AND PM10 WIDGETS INITIALIZATION--------##
        #Initialize the four pyqtgraph widget to use TimeAxisItem class
        self.graphWidget_temp = PlotWidget(self.widget,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphWidget_temp.setEnabled(False)
        self.graphWidget_temp.setObjectName("graphWidget_temp")
        self.verticalLayout.addWidget(self.graphWidget_temp)

        self.graphWidget_humi = PlotWidget(self.widget,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphWidget_humi.setEnabled(False)
        self.graphWidget_humi.setObjectName("graphWidget_humi")
        self.verticalLayout.addWidget(self.graphWidget_humi)

        self.graphWidget_pm25 = PlotWidget(self.widget,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphWidget_pm25.setEnabled(False)
        self.graphWidget_pm25.setObjectName("graphWidget_pm25")
        self.verticalLayout.addWidget(self.graphWidget_pm25)

        self.graphWidget_pm10 = PlotWidget(self.widget,axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphWidget_pm10.setEnabled(False)
        self.graphWidget_pm10.setObjectName("graphWidget_pm10")
        self.verticalLayout.addWidget(self.graphWidget_pm10)

        self.Init_graph(self.graphWidget_temp,'Temperature (°C)','',[0, 40])#"\u03BCg/m"+u'\u00B3'
        self.Init_graph(self.graphWidget_humi,'Humidity (%)','',[20, 80])
        self.Init_graph(self.graphWidget_pm25,'PM2.5 ('+"\u03BCg/m"+u'\u00B3'+')','',[0, 15])
        self.Init_graph(self.graphWidget_pm10,'PM10 ('+"\u03BCg/m"+u'\u00B3'+')','Time',[0, 20])

        self.t = np.array([timestamp()])
        self.x_temp = np.array([15])
        self.x_humi = np.array([50])
        self.x_pm25 = np.array([0])
        self.x_pm10 = np.array([0])
        self.dl_temp = self.Init_plot(self.t, self.x_temp,self.graphWidget_temp,(187, 143, 206)) # get a reference for the line
        self.dl_humi = self.Init_plot(self.t, self.x_humi,self.graphWidget_humi,(93, 173, 226)) # get a reference for the line
        self.dl_pm25 = self.Init_plot(self.t, self.x_pm25,self.graphWidget_pm25,( 35, 155, 86 )) # get a reference for the line
        self.dl_pm10 = self.Init_plot(self.t, self.x_pm10,self.graphWidget_pm10,( 25, 111, 61 )) # get a reference for the line

        # initialize the ploting labels
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_temp.setFont(font)
        self.label_humi.setFont(font)
        self.label_pm25.setFont(font)
        self.label_pm10.setFont(font)
        self.label_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.label_humi.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pm25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pm10.setAlignment(QtCore.Qt.AlignCenter)

        
        # initialize the timer for the dynamical update
        self.sensorreader = Sensorreader(self)

        #saving csv path
        self.is_record = False # whether start to record
        self.fpath = None
        self._dhtfn = 'dht_rec.csv'
        self.dhtfn = None
        
        # signals and slots
        self.pushButton_read.clicked.connect(self.read_sensor)
        self.pushButton_stop.clicked.connect(self.stop_sensor)
        self.pushButton_record.clicked.connect(self.open_file_folder_dialog)
        self.sensorreader.data_sensor.connect(self.update_plot_data)
        self.sensorreader.data_sensor.connect(self.record_sensor)
        

        ##--------CALENDAR WIDGET INITIALIZATION--------##

        #google calendar backend initialization
        self._cache_events = []
        self._backend = CalendarBackend()
        t = datetime.datetime.utcnow()
        t = t.strftime("%Y-%m-%d")+'T'+t.strftime("%H:%M:%S")+'Z'
        self.kw = {'calendarId': 'primary', 'maxResults': 50, 'orderBy': 'startTime', 'singleEvents': True, 'timeMin': t}
        self._backend.updateListEvents(self.kw)
        # signals and slots
        self._backend.eventsChanged.connect(self._handleevents)

        #calendar print year month widget initialization
        font = QtGui.QFont()
        font.setPointSize(16)
        self.CalendarText_dmy.setFont(font)
        self.CalendarText_dmy.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CalendarText_d.setFrameShape(QtWidgets.QFrame.NoFrame)
        sheetstyle = 'QTextEdit { background-color: rgb'+str(self.bgcolor.getRgb()[0:3])+'}' # set the background color
        self.CalendarText_dmy.setStyleSheet(sheetstyle)
        self.CalendarText_d.setStyleSheet(sheetstyle)
        
        #calendar widget initialization
        self.calendarWidget.selectionChanged.connect(self._loadevents)
        
        #calendar event widget initialization
        self.listWidget.clear()
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        sheetstyle = 'background-color: rgb'+str(self.bgcolor.getRgb()[0:3])
        self.listWidget.setStyleSheet(sheetstyle)
        self._loadevents()# not sure why it doesn't display the events (the events is not uploaded even with the sleep)

        ##--------PHOTO LABLE INITIALIZATION--------##
        pixmap = QtGui.QPixmap('../imgs_private/photolabel1.jpg')
        self.photolabel_1.setPixmap(pixmap.scaled(self.layoutWidget1.width(),self.layoutWidget1.height(),QtCore.Qt.KeepAspectRatio))
        pixmap = QtGui.QPixmap('../imgs_private/photolabel4.jpg')
        self.photolabel_2.setPixmap(pixmap.scaled(self.layoutWidget1.width(),self.layoutWidget1.height(),QtCore.Qt.KeepAspectRatio))
        pixmap = QtGui.QPixmap('../imgs_private/photolabel3.jpg')
        self.photolabel_3.setPixmap(pixmap.scaled(self.layoutWidget1.width(),self.layoutWidget1.height(),QtCore.Qt.KeepAspectRatio))
        # pixmap = QtGui.QPixmap('./imgs/photolabel4.jpg')
        # self.photolabel_4.setPixmap(pixmap.scaled(self.layoutWidget1.width()/4,self.layoutWidget1.height(),QtCore.Qt.KeepAspectRatio))

        pixmap = QtGui.QPixmap('./imgs/temp.png')
        self.photolabel_temp.setPixmap(pixmap.scaled(self.layoutWidget_2.width()/4,self.layoutWidget_2.height(),QtCore.Qt.KeepAspectRatio))
        self.photolabel_temp.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap('./imgs/humidity.png')
        self.photolabel_humi.setPixmap(pixmap.scaled(self.layoutWidget_2.width()/4,self.layoutWidget_2.height(),QtCore.Qt.KeepAspectRatio))
        self.photolabel_humi.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap('./imgs/pm2.5.png')
        self.photolabel_pm25.setPixmap(pixmap.scaled(self.layoutWidget_2.width()/4,self.layoutWidget_2.height(),QtCore.Qt.KeepAspectRatio))
        self.photolabel_pm25.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap('./imgs/pm2.5.png')
        self.photolabel_pm10.setPixmap(pixmap.scaled(self.layoutWidget_2.width()/4,self.layoutWidget_2.height(),QtCore.Qt.KeepAspectRatio))
        self.photolabel_pm10.setAlignment(QtCore.Qt.AlignCenter)

    def Init_plot(self, x, y, graph, color):
        '''
        Initialize the plot
        Input parameters:
            - x: 1D numpy
            - y: 1D numpy
            - graph: pyqtgraph
            - color 3x1 tuple
        Output
            - graph.plot
        '''
        # 'Line color, width & style'
        # pen = pg.mkPen(color=(10, 0, 0))
        # pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        pen = pg.mkPen(color=color, width=3)
        dl = graph.plot(x, y, pen=pen)
        return dl

    def Init_graph(self, graph, xlabel, ylabel, ylim):
        '''
        graphWidget initialization
        Input parameters:
            - graph: pyqtgraph
            - xlabel: string
            - ylabel: string
            - ylim: 2x1 float array
        '''
        #self.graphWidget.setBackground(QtGui.QColor(100, 50, 254, 25))# the color could be specify by the QtGui.
        # 'background color'
        graph.setBackground(self.bgcolor)
        # set the title
        # graph.setTitle("Your Title Here")
        # labels
        styles = {'color':'k', 'font-size':'15px'}
        graph.setLabel('left', xlabel, **styles)
        graph.setLabel('bottom', ylabel, **styles)
        # grid
        graph.showGrid(x=True, y=True)
        # X,Yrange
        graph.setXRange(timestamp(), timestamp() + 3600, padding=0)
        graph.setYRange(ylim[0], ylim[1], padding=0.1)

    def update_plot_data(self,data):
        '''
        Update the pyqtgraph plot, called by thread
        Input:
            - data: 4x1 tuple temperature; humidity ; pm2.5; pm10.
        '''
        humidity, temperature,pm25,pm10 = data
        # update labels
        self.label_temp.setText("{:.1f}".format(temperature)+u"\N{DEGREE SIGN}"+"C")
        self.label_humi.setText("{:.0f}%".format(humidity))
        self.label_pm25.setText("{:.1f}".format(pm25)+"\u03BCg/m"+u'\u00B3')
        self.label_pm10.setText("{:.1f}".format(pm10)+"\u03BCg/m"+u'\u00B3')
        # update figures
        self.t = np.append(self.t, timestamp())
        self.x_temp = np.append(self.x_temp, temperature)
        self.x_humi = np.append(self.x_humi, humidity)
        self.x_pm25 = np.append(self.x_pm25, pm25)
        self.x_pm10 = np.append(self.x_pm10, pm10)

        self.dl_temp.setData(self.t, self.x_temp) # update the line
        self.dl_humi.setData(self.t, self.x_humi) # update the line
        self.dl_pm25.setData(self.t, self.x_pm25) # update the line
        self.dl_pm10.setData(self.t, self.x_pm10) # update the line

        if (self.t[-1]-self.t[0])>3600:
            self.graphWidget_temp.setXRange(self.t[-1]-3600+5,self.t[-1]+5, padding=0)
            self.graphWidget_humi.setXRange(self.t[-1]-3600+5,self.t[-1]+5, padding=0)
            self.graphWidget_pm25.setXRange(self.t[-1]-3600+5,self.t[-1]+5, padding=0)
            self.graphWidget_pm10.setXRange(self.t[-1]-3600+5,self.t[-1]+5, padding=0)

    def read_sensor(self):
        self.sensorreader.init_flags()
        self.sensorreader.start()
        
    def stop_sensor(self):
        self.sensorreader.kill()
        self.is_record = False

    def open_file_folder_dialog(self):
        self.fpath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dhtfn = os.path.join(self.fpath,self._dhtfn)
        self.is_record=True
        print(self.dhtfn)

    def record_sensor(self,data):
        if self.is_record:
            t = datetime.datetime.now()
            data = [t.strftime("%Y-%m-%d %H:%M:%S"),data[0],data[1]]# cast into array
            if os.path.exists(self.dhtfn):
                df = pd.read_csv(self.dhtfn)
                if df.empty:
                    with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['time','humidity','temperature','PM2.5','PM10'])
                        
                        csvw.writerow(data)
                else:
                    with open(self.dhtfn, 'a') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(data)
            else:
                with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['time','humidity','temperature','PM2.5','PM10'])
                        csvw.writerow(data)
            f.close()

    def _dispdate(self):
        '''
        Convert the selected dat in the calendar to a readable string.
        Called by _loadevents function
        Output:
            - sdate: str selected date
        '''
        sdate = self.calendarWidget.selectedDate()
        d = sdate.toString('d')
        dddd = sdate.toString('dddd')
        mmmmyyyy = sdate.toString('MMMM yyyy')
        self.CalendarText_d.setText(d)
        self.CalendarText_dmy.setText(dddd+'\n'+mmmmyyyy)
        return sdate


    def _addevent(self,event):
        '''
        Add the event to the calendar list widget with neat format
        Call by _loadevents function
        Input:
            - event: a 2x1 list containing two strings
        '''

        title,time = event

        item = QtWidgets.QListWidgetItem()
        item.setText(title)
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(237, 212, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        # item.setFlags(QtCore.Qt.NoItemFlags)
        self.listWidget.addItem(item)

        item = QtWidgets.QListWidgetItem()
        item.setText(time+'\n')
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(136, 138, 133))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        # item.setFlags(QtCore.Qt.NoItemFlags)
        self.listWidget.addItem(item)

    def _loadevents(self):
        '''
        load and display events in selected date
        '''
        self.listWidget.clear()

        sdate = self._dispdate()
        sevents = []
        for event in self._cache_events:
            start = event['start']
            if start.date()==sdate:
                sevents.append(event)
        #obtain events based on the selected date
        
        for event in sevents:
            e = [event['summary'],event['start'].time().toString('hh:mm AP')+'-'+event['end'].time().toString('hh:mm AP')]
            self._addevent(e)

    def _handleevents(self, events):
        '''
        preserve events info requested from google calendar backend
        Inputs
            - events: dict
        '''
        self._cache_events = events

# todo: 1. organize the code (finish the mainwindow.py, to work on CalendarBackend.py)
#       2. not sure why the events not loaded once the window is open.
