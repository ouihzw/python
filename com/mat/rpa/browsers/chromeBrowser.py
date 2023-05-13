from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ChromeBrowser(object):
    __instance = None  # 储存浏览器引用，防止自动回收

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(ChromeBrowser, cls).__new__(cls)
        return cls.__instance

    def __init__(self):  # 将每个浏览器都创建唯一一个WebDriver对象
        options = Options()
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.chromeClient = webdriver.Chrome(options=options)

    def __del__(self):
        self.chromeClient.quit()
