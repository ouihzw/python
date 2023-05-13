# -*- coding:utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'study',#数据库名称
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': 3306,
    },
    'sqliteDB': {
        'ENGINE': 'sqlite',
        # 'NAME': os.path.join(BASE_DIR, r'com\mat\rpa\sqliteDB\db.sqlite3')
        'NAME': r'./RpaRobot.db',
    },
    'MongoDB': {
        'ENGINE': 'mongodb',
        'HOST': 'localhost',
        'PORT': 27017,
        'NAME': 'rpa'
    }
}

DATABASE_APPS_MAPPING = {
    "defaultApp" : "default" #应用与数据库配置的映射
}
