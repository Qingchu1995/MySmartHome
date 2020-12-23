import time
import datetime

def timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))
