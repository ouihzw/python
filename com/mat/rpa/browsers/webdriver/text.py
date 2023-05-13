from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # 键盘按键操作
from os import path
import csv


def spider(url, keyword):
    # 创建浏览器对象
    drver = webdriver.Chrome()
    # 浏览器访问地址
    drver.get(url)
    # 隐式等待，确保动态内容节点被完全加载出来——时间感受不到
    drver.implicitly_wait(3)
    # 最大化浏览器窗口，主要是防止内容被遮挡
    drver.maximize_window()
    # 通过id=key定位到搜索框
    input_search = drver.find_element(By.ID, "key")
    # 在输入框中输入“口罩”
    input_search.send_keys(keyword)
    # 模拟键盘回车Enter操作进行搜索
    input_search.send_keys(Keys.ENTER)
    # 强制等待3秒
    sleep(3)
    # 抓取商品数据
    get_good(drver)
    # 退出关闭浏览器
    drver.quit()

# 抓取商品数据
def get_good(driver):
    # 获取当前第一页所有商品的li标签
    goods = driver.find_elements(By.CLASS_NAME, 'gl-item')
    data = []
    for good in goods:
        # 获取商品链接
        link = good.find_element(By.TAG_NAME, 'a').get_attribute('href')
        # 获取商品标题名称
        title = good.find_element(By.CSS_SELECTOR, '.p-name em').text.replace('\n', '')
        # 获取商品价格
        price = good.find_element(By.CSS_SELECTOR, '.p-price strong').text.replace('\n', '')
        # 获取商品评价数量
        commit = good.find_element(By.CSS_SELECTOR, '.p-commit a').text
        # 将商品数据存入字典
        good_data = {
            '商品标题':title,
            '商品价格':price,
            '商品链接':link,
            '评论量':commit
        }
        data.append(good_data)
    saveCSV(data)


# 保存商品数据到CSV文件中
def saveCSV(data):
    # 表头
    header = ['商品标题', '商品价格', '商品链接', '评论量']
    # 获取当前文件路径
    paths = path.dirname(__file__)
    # 将当前文件路径与文件名拼接起来作为商品数据的存储路径
    file = path.join(paths, 'good_data.csv')
    # 以追加写入的方式将商品数据保存到文件中
    with open(file, 'a+', encoding='utf-8', newline='') as wf:
        f_csv = csv.DictWriter(wf, header)
        f_csv.writeheader()
        f_csv.writerows(data)


# 判断文件程序入口
if __name__ == '__main__':
    # 京东商城网址
    url = 'https://www.jd.com/'
    # 搜索关键字“女士编包”
    keyword = 'python'
    # 爬取数据
    spider(url, keyword)
