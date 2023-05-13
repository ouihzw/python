from com.mat.rpa.browsers import chromeBrowser
from com.mat.rpa.browsers import firefoxBrowser
from com.mat.rpa.browsers import _360ChromeBrowser
import psutil

class WebSingleClass(object):
    __instance = None  # 单例模式
    chrome = None  # chrome client
    firefox = None  # firefox client
    _360Chrom = None # 360 client
    webObject = {}

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(WebSingleClass, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    def getChromeClient(self):
        if not self.chrome:
            self.chrome = chromeBrowser.ChromeBrowser().chromeClient
        else:
            driver_process = psutil.Process(self.chrome.service.process.pid)
            if driver_process.is_running():
                #print("driver is running")
                chrome_process = driver_process.children()
                if chrome_process:
                    chrome_process = chrome_process[0]
                    if chrome_process.is_running():
                        #print("Chrome is still running, we can quit")
                        return self.chrome
                    else:
                        #print("Chrome is dead, can't quit. Let's kill the driver")
                        chrome_process.kill()
                #print("driver has died")
            self.chrome = chromeBrowser.ChromeBrowser().chromeClient
        return self.chrome

    def getFirefoxClient(self):
        if not self.firefox:
            self.firefox = firefoxBrowser.FirefoxBrowser().firefoxClient
        else:
            driver_process = psutil.Process(self.firefox.service.process.pid)
            if driver_process.is_running():
                #print("driver is running")
                firefox_process = driver_process.children()
                if firefox_process:
                    firefox_process = firefox_process[0]
                    if firefox_process.is_running():
                        #print("firefox is still running, we can quit")
                        return self.firefox
                    else:
                        #print("firefox is dead, can't quit. Let's kill the driver")
                        firefox_process.kill()
                #print("driver has died")
            self.firefox = firefoxBrowser.FirefoxBrowser().firefoxClient
        return self.firefox

    def get360Client(self):
        if not self._360Chrom:
            self._360Chrom = _360ChromeBrowser._360ChromeBrowser()._360ChromeClient
        else:
            driver_process = psutil.Process(self._360Chrom.service.process.pid)
            if driver_process.is_running():
                # print("driver is running")
                _360Chrome_process = driver_process.children()
                if _360Chrome_process:
                    _360Chrome_process = _360Chrome_process[0]
                    # if _360Chrome_process.is_running():
                    #     # print("360 is still running, we can quit")
                    #     return self._360Chrom
                    # else:
                    #     # print("360 is dead, can't quit. Let's kill the driver")
                    _360Chrome_process.kill()
                # print("driver has died")
            self._360Chrom = _360ChromeBrowser._360ChromeBrowser()._360ChromeClient
        return self._360Chrom

