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

from CalendarBackend import CalendarBackend

import pigpio
import libraries.DHT22 as DHT22
class DHTreader(QtCore.QThread):
    '''
    The class (thread) to read the DHT22 sensor.
    '''
    
    data_sensor = QtCore.pyqtSignal(tuple)
    is_killed=False
    DHT2_PIN = 4
    pi = pigpio.pi()
    dht22 = DHT22.sensor(pi,4)

    def run(self):
        while True:
            if self.is_killed:
                break
            time.sleep( 2 )
            # humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
            self.dht22.trigger()
            humidity = self.dht22.humidity()/1.0#np.random.rand(1)
            temperature = self.dht22.temperature()/1.0#np.random.rand(1)
            self.data_sensor.emit((humidity, temperature))
    def kill(self):
        self.is_killed=True
    def init_flags(self):
        self.is_killed=False

# class TimeAxisItem(pg.AxisItem):
#     def __init__(self, *args, **kwargs):
#         super(TimeAxisItem, self).__init__(*args, **kwargs)
    
#     def int2td(self, ts):
#         return(datetime.timedelta(seconds=float(ts)/1e6))

#     def tickStrings(self, values, scale, spacing):
#         print("hahaha")
#         print(values)
#         return [value.strftime("%H:%M:%S") for value in values]

# class DHTreader(QtCore.QThread):
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
#             self.data_sensor.emit((humidity[0], temperature[0]))
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

        ##--HUMIDITY and TEMPERATURE WIDGETS INITIALIZATION--##
        self.Init_graph(self.graphWidget_temp,'Temperature (°C)','',[0, 50])
        self.Init_graph(self.graphWidget_humi,'Humidity (%)','Hour (hr)',[0, 100])
        self.t = np.array([0])
        self.x_temp = np.array([15])
        self.x_humi = np.array([50])
        self.dl_temp = self.Init_plot(self.t, self.x_temp,self.graphWidget_temp) # get a reference for the line
        self.dl_humi = self.Init_plot(self.t, self.x_humi,self.graphWidget_humi) # get a reference for the line
        
        # initialize the timer for the dynamical update
        self.dhtreader = DHTreader(self)

        #saving csv path
        self.is_record = False # whether start to record
        self.fpath = None
        self._dhtfn = 'dht_rec.csv'
        self.dhtfn = None
        
        # signals and slots
        self.pushButton_read.clicked.connect(self.read_dht22)
        self.pushButton_stop.clicked.connect(self.stop_dht22)
        self.pushButton_record.clicked.connect(self.open_file_folder_dialog)
        self.dhtreader.data_sensor.connect(self.update_plot_data)
        self.dhtreader.data_sensor.connect(self.record_eht22)


        ##--CALENDAR WIDGET INITIALIZATION--##

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
        


    def Init_plot(self, x, y, graph):
        '''
        Initialize the plot
        Input parameters:
            - x: 1D numpy
            - y: 1D numpy
            - graph: pyqtgraph
        Output
            - graph.plot
        '''
        # 'Line color, width & style'
        # pen = pg.mkPen(color=(10, 0, 0))
        # pen = pg.mkPen(color=(255, 0, 0), width=15, style=QtCore.Qt.DashLine)
        pen = pg.mkPen(color=(255, 0, 0), width=5)
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
        graph.setXRange(0, 55, padding=0)
        graph.setYRange(ylim[0], ylim[1], padding=0.1)
        # graph.getPlotItem().axes['bottom']['item'] = TimeAxisItem(orientation='bottom')

    def update_plot_data(self,data):
        '''
        Update the pyqtgraph plot, called by thread
        Input:
            - data: 2x1 tuple humidity ; temperature
        '''
        humidity, temperature = data
        self.t = np.append(self.t, self.t[-1]+1)
        # self.t = np.append(self.t, datetime.datetime.now())
        self.x_temp = np.append(self.x_temp, temperature)
        self.x_humi = np.append(self.x_humi, humidity)
        self.dl_temp.setData(self.t, self.x_temp) # update the line
        self.dl_humi.setData(self.t, self.x_humi) # update the line
        initxlim = 50
        if self.t[-1]>initxlim:
            self.graphWidget_temp.setXRange(self.t[-1]-initxlim+5,self.t[-1]+5, padding=0)
            self.graphWidget_humi.setXRange(self.t[-1]-initxlim+5,self.t[-1]+5, padding=0)

    def read_dht22(self):
        self.dhtreader.init_flags()
        self.dhtreader.start()
        
    def stop_dht22(self):
        self.dhtreader.kill()
        self.is_record = False

    def open_file_folder_dialog(self):
        self.fpath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dhtfn = os.path.join(self.fpath,self._dhtfn)
        self.is_record=True
        print(self.dhtfn)

    def record_eht22(self,data):
        if self.is_record:
            t = datetime.datetime.now()
            data = [t.strftime("%Y-%m-%d %H:%M:%S"),data[0],data[1]]# cast into array
            if os.path.exists(self.dhtfn):
                df = pd.read_csv(self.dhtfn)
                if df.empty:
                    with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['time','humidity','temperature'])
                        
                        csvw.writerow(data)
                else:
                    with open(self.dhtfn, 'a') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(data)
            else:
                with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['time','humidity','temperature'])
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
#       2. the time axis in temperature and humidity sensing
#       3. not sure why the events not loaded once the window is open.