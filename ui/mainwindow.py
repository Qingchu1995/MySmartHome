# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
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

import pigpio
import DHT22
class DHTreader(QtCore.QThread):
    
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
            dht22.trigger()
            humidity = dht22.humidity#np.random.rand(1)
            temperature = dht22.temperature#np.random.rand(1)
            self.data_sensor.emit((humidity, temperature))

    def kill(self):
        self.is_killed=True
    def init_flags(self):
        self.is_killed=False



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
        
        # signal and slot
        self.pushButton_read.clicked.connect(self.read_dht22)
        self.pushButton_stop.clicked.connect(self.stop_dht22)
        self.pushButton_record.clicked.connect(self.open_file_folder_dialog)
        self.dhtreader.data_sensor.connect(self.update_plot_data)
        self.dhtreader.data_sensor.connect(self.record_eht22data)
        

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

    def Init_graph(self, graph,xlabel,ylabel,ylim):
        '''
        graphWidget_temp initialization
        Input parameters:
            - graph: pyqtgraph
            - xlabel: string
            - ylabel: string
        '''
        #self.graphWidget_temp.setBackground(QtGui.QColor(100, 50, 254, 25))# the color could be specify by the QtGui.
        # 'background color'
        color = self.palette().color(QtGui.QPalette.Window)  # Get the default window background,
        graph.setBackground(color)
        # set the title
        # graph.setTitle("Your Title Here")
        # labels
        styles = {'color':'k', 'font-size':'15px'}
        graph.setLabel('left', xlabel, **styles)
        graph.setLabel('bottom', ylabel, **styles)
        # grid
        graph.showGrid(x=True, y=True)
        # X,Yrange
        graph.setXRange(0, 1000, padding=0)
        graph.setYRange(ylim[0], ylim[1], padding=0.1)

    def update_plot_data_test(self):
        '''
        Update the pyqtgraph plot, called by Qtimer
        '''

        self.t = np.append(self.t, self.t[-1]+1)
        self.x_temp = np.append(self.x_temp, np.sin(time.time()))
        self.x_humi = np.append(self.x_humi, np.sin(time.time()))
        self.dl_temp.setData(self.t, self.x_temp) # update the line
        self.dl_humi.setData(self.t, self.x_humi) # update the line
        if self.t[-1]>900:
            self.graphWidget_temp.setXRange(self.t[-1]-1000+100,self.t[-1]+100, padding=0)
            self.graphWidget_humi.setXRange(self.t[-1]-1000+100,self.t[-1]+100, padding=0)

    def update_plot_data(self,data):
        '''
        Update the pyqtgraph plot, called by Qtimer
        Input:
            - data: 2x1 tuple humidity ; temperature
        '''
        humidity, temperature = data
        self.t = np.append(self.t, self.t[-1]+1)
        self.x_temp = np.append(self.x_temp, temperature)
        self.x_humi = np.append(self.x_humi, humidity)
        self.dl_temp.setData(self.t, self.x_temp) # update the line
        self.dl_humi.setData(self.t, self.x_humi) # update the line
        if self.t[-1]>900:
            self.graphWidget_temp.setXRange(self.t[-1]-1000+100,self.t[-1]+100, padding=0)
            self.graphWidget_humi.setXRange(self.t[-1]-1000+100,self.t[-1]+100, padding=0)

    def read_dht22(self):
        self.dhtreader.init_flags()
        self.dhtreader.start()
        
    def resume_dht22(self):
        self.dhtreader.pause()

    def stop_dht22(self):
        self.dhtreader.kill()

    def open_file_folder_dialog(self):
        self.fpath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dhtfn = os.path.join(self.fpath,self._dhtfn)
        self.is_record=True
        print(self.dhtfn)

    def record_eht22data(self,data):
        if self.is_record:
            data = [data[0][0],data[1][0]]# cast into array
            if os.path.exists(self.dhtfn):
                df = pd.read_csv(self.dhtfn)
                if df.empty:
                    with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['humidity','temperature'])
                        
                        csvw.writerow(data)
                else:
                    with open(self.dhtfn, 'a') as f:
                        csvw = csv.writer(f, delimiter=',')
                        # csvw.writerow(['humidity','temperature'])
                        csvw.writerow(data)
            else:
                with open(self.dhtfn, 'w') as f:
                        csvw = csv.writer(f, delimiter=',')
                        csvw.writerow(['humidity','temperature'])
                        csvw.writerow(data)


