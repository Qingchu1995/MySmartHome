import logging
import os
import pickle
import sys
import threading

from PyQt5 import QtCore, QtGui

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


logging.basicConfig(level=logging.DEBUG)


class CalendarBackend(QtCore.QObject):
    eventsChanged = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._service = None

    @property
    def service(self):
        return self._service

    def updateListEvents(self, kw):
        threading.Thread(target=self._update_list_events, args=(kw,)).start()

    def _update_list_events(self, kw):
        self._update_credentials()
        # print(kw)
        events_result = self.service.events().list(**kw).execute()
        # for event in events_result['items']:
        #     print(event['summary'])
        events = events_result.get("items", [])
        # print(events)

        qt_events = []
        if not events:
            logging.debug("No upcoming events found.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            # logging.debug(f"From {start} - To {end}:  {event['summary']}")

            start_dt = QtCore.QDateTime.fromString(start, QtCore.Qt.ISODate)
            end_dt = QtCore.QDateTime.fromString(end, QtCore.Qt.ISODate)
            summary = event["summary"]

            e = {"start": start_dt, "end": end_dt, "summary": summary}
            qt_events.append(e)

        self.eventsChanged.emit(qt_events)

    def _update_credentials(self):
        creds = None
        if os.path.exists("../token/token.pickle"):
            with open("../token/token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "../token/credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("../token/token.pickle", "wb") as token:
                pickle.dump(creds, token)

        self._service = build("calendar", "v3", credentials=creds, cache_discovery=False)
