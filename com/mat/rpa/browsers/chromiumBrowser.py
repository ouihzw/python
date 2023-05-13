from selenium import webdriver

class ChromeBrowser(object):
    __instance = None  # 储存浏览器引用，防止自动回收

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(ChromeBrowser, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.chromeClient = webdriver.Chrome()


    def __del__(self):
        self.chromeClient.quit()
