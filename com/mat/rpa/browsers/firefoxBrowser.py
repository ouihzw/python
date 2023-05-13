from selenium import webdriver


class FirefoxBrowser(object):
    __instance = None  # 储存浏览器引用，防止自动回收

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(FirefoxBrowser, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.firefoxClient = webdriver.Firefox(firefox_binary="./com/mat/rpa/browsers/firefox-core/firefox.exe",
                                               executable_path="./com/mat/rpa/browsers/webdriver/geckodriver.exe")

    def __del__(self):
        self.firefoxClient.quit()
