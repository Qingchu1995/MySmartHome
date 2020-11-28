from PyQt5 import QtWidgets
from ui.mainwindow import MainWindow
import sys
import numpy as np
import random
import os

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    
if __name__ == "__main__":
    seed_everything(seed=42)
    main()
    
