from PyQt5 import QtWidgets
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        with requests.Session() as self.req:
            retry = Retry(connect=4, backoff_factor=0.3)
            adapter = HTTPAdapter(max_retries=retry)
            self.req.mount('https://www.everytime.kr', adapter)

    def init(self, render, signal, slot, requestHandle):
        self.Render = render
        self.Signal = signal
        self.Slot = slot
        self.RequestHandle = requestHandle
        self.threadCount = 4
        self.mine = None # My articles and comments
        self.searching = False