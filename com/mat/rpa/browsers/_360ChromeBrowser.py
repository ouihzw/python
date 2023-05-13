from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

class _360ChromeBrowser(object):
    __instance = None  # 储存浏览器引用，防止自动回收

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(_360ChromeBrowser, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        # 创建ChromeDriver实例，启动360安全浏览器
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.getcwd() + "\\com\\mat\\rpa\\browsers\\360se6\\Application\\360se.exe"  # 360浏览器的路径
        chrome_options.add_argument(r'--lang=zh-CN')  # 这里添加一些启动的参数
        path = os.getcwd() + "\\com\\mat\\rpa\\browsers\\webdriver\\chromedriver.exe"
        s = Service(path)
        self._360ChromeClient = webdriver.Chrome(options=chrome_options, service=s)

    def __del__(self):
        self._360ChromeClient.quit()